from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
FINISH_ROOT = ROOT.parent

from renzo.app.workflow_failures import classify_workflow_failure
from renzo.app.runtime_env import build_runtime_env, find_conda_bin


class _SafeFormatDict(dict[str, Any]):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def _render_text(value: Any, context: dict[str, Any], *, allow_missing: bool = False) -> str:
    if isinstance(value, str):
        if allow_missing:
            return value.format_map(_SafeFormatDict(context))
        return value.format(**context)
    return str(value)


def _load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in config file: {path}")
    return data


def _ensure_paths(base_dir: Path, paths: list[str]) -> None:
    for raw in paths:
        path = _resolve_runtime_path(base_dir, raw)
        if not path.exists():
            raise FileNotFoundError(f"Missing required path: {raw}")


def _runtime_base_candidates(base_dir: Path) -> list[Path]:
    candidates = [base_dir]
    original_workflow_root = (FINISH_ROOT / base_dir.name).resolve()
    if original_workflow_root not in candidates:
        candidates.append(original_workflow_root)
    return candidates


def _resolve_runtime_path(base_dir: Path, raw: str) -> Path:
    text = str(raw).strip()
    candidate = Path(text)
    if candidate.is_absolute():
        return candidate.resolve()
    for root in _runtime_base_candidates(base_dir):
        resolved = (root / text).resolve()
        if resolved.exists():
            return resolved
    return (base_dir / text).resolve()


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        text = str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return ordered


def _expand_targets_from_table(specs: Any, base_dir: Path, context: dict[str, Any]) -> list[str]:
    if not isinstance(specs, list):
        return []
    targets: list[str] = []
    for item in specs:
        if not isinstance(item, dict):
            continue
        pattern = _render_text(item.get("pattern", ""), context, allow_missing=True)
        table = _render_text(item.get("table", ""), context)
        if not pattern or not table:
            continue
        delimiter = str(item.get("delimiter", "\t"))
        table_path = _resolve_runtime_path(base_dir, table)
        with table_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            for row in reader:
                row_context = {
                    **context,
                    **{key: value for key, value in row.items() if value is not None},
                }
                try:
                    rendered = _render_text(pattern, row_context)
                except KeyError as exc:
                    raise ValueError(
                        f"Missing placeholder {exc.args[0]!r} while expanding targets_from_table from {table}"
                    ) from exc
                targets.append(rendered)
    return _dedupe_keep_order(targets)


def _normalize_scheduler(parts: list[str], scheduler: str) -> list[str]:
    if not scheduler or "--scheduler" in parts:
        return parts
    return [*parts, "--scheduler", scheduler]


def _sanitize_cache_component(value: str) -> str:
    text = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "_" for ch in str(value)).strip("._")
    return text or "default"


def _artifact_cache_root() -> Path:
    configured = os.environ.get("RENZO_SHARED_ARTIFACT_CACHE_DIR", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    base = os.environ.get("WORKFLOW_RUNTIME_BASE_CACHE_DIR", "").strip()
    if base:
        return (Path(base).expanduser().resolve() / "finish-step-artifacts").resolve()
    return (ROOT / "data" / "cache" / "runtime" / "finish-step-artifacts").resolve()


def _artifact_cache_paths(step: dict[str, Any], base_dir: Path, context: dict[str, Any]) -> list[str]:
    raw = step.get("artifact_cache")
    if not raw:
        return []
    if isinstance(raw, dict):
        paths = [_render_text(item, context) for item in (raw.get("paths") or [])]
    else:
        paths = []
    if paths:
        return _dedupe_keep_order(paths)

    nested = step.get("snakemake")
    if not isinstance(nested, dict):
        return []
    inferred = [_render_text(item, context) for item in (nested.get("targets") or [])]
    inferred.extend(_expand_targets_from_table(nested.get("targets_from_table"), base_dir, context))
    return _dedupe_keep_order(inferred)


def _artifact_cache_dir(
    *,
    step_id: str,
    step: dict[str, Any],
    base_dir: Path,
    config_path: Path,
    context: dict[str, Any],
    cache_paths: list[str],
) -> Path | None:
    if not step.get("artifact_cache") or not cache_paths:
        return None
    nested = step.get("snakemake") or {}
    payload = {
        "workflow_id": context.get("workflow_id", base_dir.name),
        "step_id": step_id,
        "cache_paths": cache_paths,
        "command": step.get("command", ""),
        "snakemake": nested,
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8"))
    digest.update(config_path.read_bytes())
    configfile = nested.get("configfile")
    if configfile:
        nested_config_path = _resolve_runtime_path(base_dir, _render_text(configfile, context))
        if nested_config_path.exists():
            digest.update(nested_config_path.read_bytes())
    cache_root = _artifact_cache_root()
    return (
        cache_root
        / _sanitize_cache_component(str(context.get("workflow_id", base_dir.name)))
        / _sanitize_cache_component(step_id)
        / digest.hexdigest()[:24]
    ).resolve()


def _path_exists(root: Path, rel_path: str) -> bool:
    return (root / rel_path).resolve().exists()


def _all_paths_exist(root: Path, paths: list[str]) -> bool:
    return bool(paths) and all(_path_exists(root, rel_path) for rel_path in paths)


def _replace_path(src: Path, dest: Path) -> None:
    if dest.exists() or dest.is_symlink():
        if dest.is_dir() and not dest.is_symlink():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    if src.is_dir():
        shutil.copytree(src, dest)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(src, dest)
    except OSError:
        shutil.copy2(src, dest)


def _restore_artifact_cache(cache_dir: Path, base_dir: Path, paths: list[str]) -> bool:
    if not _all_paths_exist(cache_dir, paths):
        return False
    for rel_path in paths:
        source = (cache_dir / rel_path).resolve()
        dest = (base_dir / rel_path).resolve()
        dest.parent.mkdir(parents=True, exist_ok=True)
        _replace_path(source, dest)
    return True


def _store_artifact_cache(cache_dir: Path, base_dir: Path, paths: list[str]) -> bool:
    if not _all_paths_exist(base_dir, paths):
        return False
    for rel_path in paths:
        source = (base_dir / rel_path).resolve()
        dest = (cache_dir / rel_path).resolve()
        dest.parent.mkdir(parents=True, exist_ok=True)
        _replace_path(source, dest)
    return True


def _build_nested_snakemake_command(spec: dict[str, Any], base_dir: Path, context: dict[str, Any]) -> list[str]:
    directory = _render_text(spec.get("directory", "."), context)
    snakefile = _render_text(spec.get("snakefile", "workflow/Snakefile"), context)
    cores = _render_text(spec.get("cores", context.get("source_cores", 1)), context)
    command = [
        sys.executable,
        "-m",
        "snakemake",
        "-s",
        str(_resolve_runtime_path(base_dir, snakefile)),
        "--directory",
        str(_resolve_runtime_path(base_dir, directory)),
        "--cores",
        str(cores),
        "--printshellcmds",
    ]
    if spec.get("use_conda"):
        command.append("--use-conda")
    configfile = spec.get("configfile")
    if configfile:
        command.extend(["--configfile", str(_resolve_runtime_path(base_dir, _render_text(configfile, context)))])
    if bool(spec.get("use_conda", False)):
        command.append("--use-conda")

    scheduler = str(spec.get("scheduler") or os.environ.get("RENZO_NESTED_SNAKEMAKE_SCHEDULER", "")).strip()
    command = _normalize_scheduler(command, scheduler)

    extra_args = spec.get("extra_args") or []
    if isinstance(extra_args, list):
        command.extend(_render_text(item, context) for item in extra_args)
    elif extra_args:
        command.extend(shlex.split(_render_text(extra_args, context)))

    targets = [
        _render_text(item, context)
        for item in (spec.get("targets") or [])
    ]
    targets.extend(_expand_targets_from_table(spec.get("targets_from_table"), base_dir, context))
    targets = _dedupe_keep_order(targets)
    if targets:
        command.extend(targets)
        return command

    until = [_render_text(item, context) for item in (spec.get("until") or [])]
    until = _dedupe_keep_order(until)
    if until:
        command.extend(["--until", *until])
        root_target = _render_text(spec.get("root_target", ""), context).strip()
        if root_target:
            command.append(root_target)
    return command


def _build_legacy_command(command_text: str, scheduler: str) -> list[str]:
    parts = shlex.split(command_text)
    if parts and parts[0] == "snakemake":
        parts = [sys.executable, "-m", "snakemake", *parts[1:]]
        parts = _normalize_scheduler(parts, scheduler)
    return parts


def _wrap_with_conda_env(command: list[str], env_name: str) -> list[str]:
    text = str(env_name or "").strip()
    if not text:
        return command
    conda_bin = find_conda_bin(os.environ.get("CONDA_EXE"))
    if not conda_bin:
        return command
    return [conda_bin, "run", "-n", text, *command]


def _build_command(step: dict[str, Any], base_dir: Path, context: dict[str, Any]) -> tuple[list[str], str]:
    nested = step.get("snakemake")
    if isinstance(nested, dict):
        command = _build_nested_snakemake_command(nested, base_dir, context)
        return command, shlex.join(command)
    command_text = _render_text(step.get("command", ""), context)
    scheduler = str(os.environ.get("RENZO_NESTED_SNAKEMAKE_SCHEDULER", "")).strip()
    command = _build_legacy_command(command_text, scheduler)
    command_env = (
        step.get("command_conda_env")
        or step.get("shared_conda_env")
        or context.get("command_conda_env")
        or context.get("shared_conda_env")
        or ""
    )
    command = _wrap_with_conda_env(command, _render_text(command_env, context, allow_missing=True))
    return command, shlex.join(command) if command else command_text


def _build_step_context(config: dict[str, Any], step_id: str, step: dict[str, Any], base_dir: Path | None = None) -> dict[str, Any]:
    context = dict(config)
    context["step_id"] = step_id
    context.setdefault("workflow_id", config.get("workflow_id"))
    source_cores = step.get("source_cores", config.get("source_cores", 8))
    context["source_cores"] = source_cores
    if base_dir is not None:
        context["workflow_dir"] = str(base_dir.resolve())
    # Resolve top-level scalar templates like "{workflow_dir}/..." before step-level
    # command rendering so nested placeholders do not leak into the executed command.
    for _ in range(2):
        changed = False
        for key, value in list(context.items()):
            if not isinstance(value, str) or "{" not in value:
                continue
            rendered = _render_text(value, context, allow_missing=True)
            if rendered != value:
                context[key] = rendered
                changed = True
        if not changed:
            break
    return context


def _write_stamp(output_path: Path, step_id: str, command_text: str, attempts: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        f"{step_id}\n{command_text}\nattempts={attempts}\n",
        encoding="utf-8",
    )


def _cleanup_wrapper_cache() -> None:
    xdg_cache_home = os.environ.get("XDG_CACHE_HOME", "").strip()
    if not xdg_cache_home:
        return
    base = Path(xdg_cache_home).resolve()
    if not base.exists():
        return
    for pattern in (
        "snakemake/**/github.com/snakemake/snakemake-wrappers",
        "snakemake/**/github.com/snakemake/snakemake-wrappers*",
    ):
        for path in base.glob(pattern):
            if path.exists():
                shutil.rmtree(path, ignore_errors=True)


def _run_with_retries(
    command: list[str],
    *,
    cwd: Path,
    retries: int,
    artifact_cache_dir: Path | None = None,
    artifact_cache_paths: list[str] | None = None,
) -> tuple[subprocess.CompletedProcess[str], int, bool]:
    attempts = 0
    delay_seconds = float(os.environ.get("RENZO_NESTED_SNAKEMAKE_RETRY_DELAY_SECONDS", "2"))
    cache_paths = artifact_cache_paths or []
    while True:
        if artifact_cache_dir is not None and cache_paths:
            if _restore_artifact_cache(artifact_cache_dir, cwd, cache_paths):
                sys.stderr.write(f"[renzo artifact cache] restored {len(cache_paths)} paths from {artifact_cache_dir}\n")
                return subprocess.CompletedProcess(command, 0, "", ""), attempts, True
        attempts += 1
        result = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            env=build_runtime_env(),
        )
        if result.stdout:
            sys.stdout.write(result.stdout)
        if result.stderr:
            sys.stderr.write(result.stderr)
        if result.returncode == 0:
            return result, attempts, False

        failure = classify_workflow_failure(result.stdout, result.stderr, work_dir=cwd)
        if attempts > retries + 1 or not failure.get("retryable"):
            return result, attempts, False

        if failure.get("code") == "snakemake_wrapper_unavailable":
            _cleanup_wrapper_cache()
        sys.stderr.write(
            f"\n[renzo nested retry] step failed with {failure['code']}; retrying attempt {attempts + 1}/{retries + 1}\n"
        )
        time.sleep(delay_seconds)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", required=True)
    parser.add_argument("--step-id", required=True)
    parser.add_argument("--output-path", required=True)
    args = parser.parse_args(argv)

    base_dir = Path.cwd().resolve()
    config_path = (base_dir / args.config_file).resolve()
    config = _load_config(config_path)
    steps = config.get("steps") or {}
    if args.step_id not in steps:
        raise KeyError(f"Step '{args.step_id}' not found in {config_path}")

    step = steps[args.step_id] or {}
    context = _build_step_context(config, args.step_id, step, base_dir=base_dir)
    required_paths = [
        _render_text(str(path), context, allow_missing=True)
        for path in (step.get("requires") or [])
        if str(path).strip()
    ]
    _ensure_paths(base_dir, required_paths)

    command, command_text = _build_command(step, base_dir, context)
    artifact_cache_paths = _artifact_cache_paths(step, base_dir, context)
    artifact_cache_dir = _artifact_cache_dir(
        step_id=args.step_id,
        step=step,
        base_dir=base_dir,
        config_path=config_path,
        context=context,
        cache_paths=artifact_cache_paths,
    )
    output_path = (base_dir / args.output_path).resolve()
    if artifact_cache_dir is not None and _all_paths_exist(base_dir, artifact_cache_paths):
        artifact_cache_dir.mkdir(parents=True, exist_ok=True)
        if _store_artifact_cache(artifact_cache_dir, base_dir, artifact_cache_paths):
            sys.stderr.write(f"[renzo artifact cache] stored {len(artifact_cache_paths)} local paths into {artifact_cache_dir}\n")
        _write_stamp(output_path, args.step_id, command_text or "[artifact-cache-local]", 0)
        return 0
    if not command:
        _write_stamp(output_path, args.step_id, command_text, 0)
        return 0

    nested = step.get("snakemake") or {}
    retries = int(
        step.get(
            "retries",
            nested.get(
                "retries",
                config.get("retries", os.environ.get("RENZO_NESTED_SNAKEMAKE_RETRIES", "0")),
            ),
        )
    )
    result, attempts, restored_from_cache = _run_with_retries(
        command,
        cwd=base_dir,
        retries=max(retries, 0),
        artifact_cache_dir=artifact_cache_dir,
        artifact_cache_paths=artifact_cache_paths,
    )
    if restored_from_cache:
        _write_stamp(output_path, args.step_id, command_text or "[artifact-cache-restore]", attempts)
        return 0
    if result.returncode != 0:
        failure = classify_workflow_failure(result.stdout, result.stderr, work_dir=base_dir)
        sys.stderr.write(
            f"\n[renzo nested failure] code={failure['code']} category={failure['category']} retryable={failure['retryable']}\n"
        )
        sys.stderr.write(f"[renzo nested failure] hint={failure['hint']}\n")
        return result.returncode

    if artifact_cache_dir is not None:
        artifact_cache_dir.mkdir(parents=True, exist_ok=True)
        if _store_artifact_cache(artifact_cache_dir, base_dir, artifact_cache_paths):
            sys.stderr.write(f"[renzo artifact cache] stored {len(artifact_cache_paths)} paths into {artifact_cache_dir}\n")
    _write_stamp(output_path, args.step_id, command_text, attempts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
