from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

import yaml


FINISH_ROOT = Path(__file__).resolve().parents[1]
ENV_SPECS_DIR = FINISH_ROOT / "sandbox" / "env_specs"
PLAN_JSON = FINISH_ROOT / "BENCHMARK_RUN_PLAN.json"
STATUS_JSON = FINISH_ROOT / "FINISH_EXPANSION_STATUS.json"
SANDBOX_STATUS_JSON = FINISH_ROOT / "SANDBOX_ENV_STATUS.json"
SANDBOX_STATUS_MD = FINISH_ROOT / "SANDBOX_ENV_STATUS.md"

sys.path.insert(0, str(FINISH_ROOT / "Renzo_DA_Agent"))
from renzo.app.runtime_env import build_runtime_env, find_conda_bin  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--skip-manual-envs", action="store_true")
    parser.add_argument("--skip-snakemake-prewarm", action="store_true")
    parser.add_argument("--exclude-command-envs", nargs="*", default=[])
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    return parser.parse_args()


def load_workflow_ids(args: argparse.Namespace) -> list[str]:
    payload = json.loads(STATUS_JSON.read_text(encoding="utf-8"))
    rows = [
        row["workflow_id"]
        for row in payload.get("rows") or []
        if str(row.get("workflow_id", "")).endswith("-finish")
    ]
    if args.only:
        wanted = set(args.only)
        rows = [wid for wid in rows if wid in wanted]
    if args.limit and args.limit > 0:
        rows = rows[: args.limit]
    return rows


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        check=False,
        cwd=str(cwd or FINISH_ROOT.parent),
        env=build_runtime_env(),
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        details = (completed.stderr or completed.stdout or "").strip()
        if len(details) > 4000:
            details = details[:4000]
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}\n{details}")
    return completed


def conda_env_names(conda_bin: str) -> set[str]:
    completed = run([conda_bin, "env", "list", "--json"])
    payload = json.loads(completed.stdout)
    names = set()
    for path in payload.get("envs", []):
        names.add(Path(path).name)
    return names


def remove_conda_env_dir(conda_bin: str, env_name: str) -> None:
    candidates = [Path(conda_bin).resolve().parents[1] / "envs" / env_name]
    custom_envs = (build_runtime_env().get("CONDA_ENVS_PATH") or "").strip()
    if custom_envs:
        for entry in custom_envs.split(os.pathsep):
            text = entry.strip()
            if text:
                candidates.append(Path(text) / env_name)
    seen: set[str] = set()
    for env_root in candidates:
        key = str(env_root.resolve()) if env_root.exists() else str(env_root)
        if key in seen:
            continue
        seen.add(key)
        if env_root.exists():
            shutil.rmtree(env_root, ignore_errors=True)


def ensure_conda_env(conda_bin: str, env_name: str, spec_path: Path) -> str:
    existing = conda_env_names(conda_bin)
    try:
        if env_name in existing:
            run([conda_bin, "env", "update", "-n", env_name, "-f", str(spec_path), "--prune"])
            return "updated"
        run([conda_bin, "env", "create", "-n", env_name, "-f", str(spec_path)])
        return "created"
    except Exception as exc:
        text = str(exc)
        if "CorruptedEnvironmentError" in text or "has been corrupted" in text:
            remove_conda_env_dir(conda_bin, env_name)
            run([conda_bin, "env", "create", "-n", env_name, "-f", str(spec_path)])
            return "recreated_after_corruption"
        raise


def collect_command_envs(workflow_ids: list[str]) -> set[str]:
    envs: set[str] = set()
    for workflow_id in workflow_ids:
        config_path = FINISH_ROOT / workflow_id / "config_basic" / "config.yaml"
        if not config_path.exists():
            continue
        config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        value = str(config.get("command_conda_env") or "").strip()
        if value:
            envs.add(value)
        for step in (config.get("steps") or {}).values():
            value = str(step.get("command_conda_env") or "").strip()
            if value:
                envs.add(value)
    return envs


def resolve_nested_path(workflow_dir: Path, raw: str | None) -> str:
    value = str(raw or "").strip()
    if not value:
        return ""
    candidate = Path(value)
    if candidate.is_absolute():
        return str(candidate)
    return str((workflow_dir / value).resolve())


def build_nested_snakemake_command(spec: dict, workflow_dir: Path, host_python: str = "python") -> list[str]:
    workdir = resolve_nested_path(workflow_dir, spec.get("directory")) or str(workflow_dir.resolve())
    command = [
        host_python,
        "-m",
        "snakemake",
        "-s",
        resolve_nested_path(workflow_dir, spec["snakefile"]),
        "--directory",
        workdir,
        "--cores",
        "1",
    ]
    configfile = str(spec.get("configfile") or "").strip()
    if configfile:
        command.extend(["--configfile", resolve_nested_path(workflow_dir, configfile)])
    if spec.get("use_conda", True):
        command.append("--use-conda")
        command.append("--conda-create-envs-only")
    scheduler = str(spec.get("scheduler") or "").strip()
    if scheduler:
        command.extend(["--scheduler", scheduler])
    root_target = str(spec.get("root_target") or "").strip()
    targets = list(spec.get("targets") or [])
    if root_target:
        command.append(root_target)
    elif targets:
        command.extend([str(x) for x in targets])
    until = list(spec.get("until") or [])
    if until:
        command.append("--until")
        command.extend([str(x) for x in until])
    return command


def prewarm_snakemake_workflow(conda_bin: str, workflow_id: str) -> None:
    workflow_dir = FINISH_ROOT / workflow_id
    config_path = workflow_dir / "config_basic" / "config.yaml"
    if not config_path.exists():
        return
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    steps = config.get("steps") or {}
    last_spec = None
    for step in steps.values():
        nested = step.get("snakemake")
        if isinstance(nested, dict):
            last_spec = nested
    if not isinstance(last_spec, dict):
        return
    if not last_spec.get("use_conda", True):
        return
    host_env = "snakemake"
    cmd = [conda_bin, "run", "-n", host_env, *build_nested_snakemake_command(last_spec, workflow_dir, host_python="python")]
    run(cmd, cwd=workflow_dir)


def classify_prewarm_failure(exc: Exception) -> tuple[bool, str]:
    text = str(exc)
    lowered = text.lower()
    if "missinginputexception" in lowered or "missing input files" in lowered:
        return True, f"prewarm_input_gated: {text}"
    return False, f"prewarm_failed: {text}"


def workflow_has_nested_snakemake(workflow_id: str) -> bool:
    config_path = FINISH_ROOT / workflow_id / "config_basic" / "config.yaml"
    if not config_path.exists():
        return False
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    for step in (config.get("steps") or {}).values():
        if isinstance(step, dict) and isinstance(step.get("snakemake"), dict):
            return True
    return False


def workflow_command_envs(workflow_id: str) -> set[str]:
    config_path = FINISH_ROOT / workflow_id / "config_basic" / "config.yaml"
    if not config_path.exists():
        return set()
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    envs: set[str] = set()
    root_value = str(config.get("command_conda_env") or "").strip()
    if root_value:
        envs.add(root_value)
    for step in (config.get("steps") or {}).values():
        value = str(step.get("command_conda_env") or "").strip()
        if value:
            envs.add(value)
    return envs


def write_status_report(payload: dict) -> None:
    SANDBOX_STATUS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Sandbox Environment Status",
        "",
        f"- 更新时间: {payload['generated_at']}",
        f"- 宿主 snakemake 环境就绪: {payload['host_env_ready']}",
        f"- special env 成功数: {payload['special_env_ready_count']}",
        f"- Snakemake prewarm 成功 workflow 数: {payload['snakemake_prewarm_ready_count']}",
        "",
        "## Special Envs",
        "",
        "| Env | Ready | Detail |",
        "|---|---|---|",
    ]
    for row in payload["special_envs"]:
        lines.append(f"| `{row['env_name']}` | {row['ready']}`` | {row['detail']} |".replace("``", ""))
    lines.extend(
        [
            "",
            "## Workflow Readiness",
            "",
            "| Workflow | Ready | Command envs | Snakemake prewarm | Detail |",
            "|---|---|---|---|---|",
        ]
    )
    for row in payload["workflow_readiness"]:
        lines.append(
            f"| `{row['workflow_id']}` | {row['ready']} | "
            f"{', '.join(row['command_envs']) or '-'} | {row['snakemake_prewarm_ready']} | {row['detail']} |"
        )
    SANDBOX_STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    conda_bin = find_conda_bin()
    workflow_ids = load_workflow_ids(args)
    excluded_envs = set(args.exclude_command_envs or [])
    special_env_status: dict[str, dict[str, str | bool]] = {}
    workflow_prewarm_status: dict[str, dict[str, str | bool]] = {}
    host_ready = False

    try:
        ensure_conda_env(conda_bin, "snakemake", ENV_SPECS_DIR / "snakemake-host.yaml")
        host_ready = True
    except Exception as exc:
        host_ready = False
        if args.strict:
            raise
        print(f"[host-env-failed] {exc}")

    if not args.skip_manual_envs:
        for env_name in sorted(collect_command_envs(workflow_ids)):
            if env_name in excluded_envs:
                special_env_status[env_name] = {"env_name": env_name, "ready": False, "detail": "excluded_by_request"}
                print(f"[skip-env] {env_name} excluded")
                continue
            spec_path = ENV_SPECS_DIR / f"{env_name}.yaml"
            if not spec_path.exists():
                special_env_status[env_name] = {"env_name": env_name, "ready": False, "detail": "missing_env_spec"}
                print(f"[skip] missing env spec for {env_name}")
                continue
            print(f"[env] {env_name}")
            try:
                mode = ensure_conda_env(conda_bin, env_name, spec_path)
                special_env_status[env_name] = {"env_name": env_name, "ready": True, "detail": mode}
            except Exception as exc:
                special_env_status[env_name] = {"env_name": env_name, "ready": False, "detail": f"create_failed: {exc}"}
                if args.strict:
                    raise

    if not args.skip_snakemake_prewarm:
        for workflow_id in workflow_ids:
            print(f"[prewarm] {workflow_id}")
            try:
                prewarm_snakemake_workflow(conda_bin, workflow_id)
                workflow_prewarm_status[workflow_id] = {"ready": True, "detail": "prewarm_ok", "input_gated": False}
            except Exception as exc:
                input_gated, detail = classify_prewarm_failure(exc)
                workflow_prewarm_status[workflow_id] = {"ready": False, "detail": detail, "input_gated": input_gated}
                if args.strict and not input_gated:
                    raise

    workflow_rows = []
    for workflow_id in workflow_ids:
        command_envs = sorted(workflow_command_envs(workflow_id))
        envs_ready = all(bool(special_env_status.get(env, {}).get("ready")) for env in command_envs if env not in excluded_envs)
        if excluded_envs.intersection(command_envs):
            envs_ready = False
        has_nested_snakemake = workflow_has_nested_snakemake(workflow_id)
        prewarm_row = workflow_prewarm_status.get(workflow_id, {})
        snakemake_ready = bool(prewarm_row.get("ready", args.skip_snakemake_prewarm))
        snakemake_input_gated = bool(prewarm_row.get("input_gated", False))
        if args.skip_snakemake_prewarm:
            snakemake_ready = False
            snakemake_input_gated = False
        snakemake_env_ok = snakemake_ready or snakemake_input_gated or not has_nested_snakemake
        detail_parts = []
        if command_envs:
            detail_parts.append("command envs ready" if envs_ready else "command envs not ready")
        else:
            detail_parts.append("no command envs")
        if not has_nested_snakemake:
            detail_parts.append("no nested snakemake")
        elif snakemake_ready:
            detail_parts.append("snakemake prewarm ready")
        elif snakemake_input_gated:
            detail_parts.append("snakemake prewarm input-gated")
        else:
            detail_parts.append("snakemake prewarm pending")
        if prewarm_row.get("detail"):
            detail_parts.append(str(prewarm_row["detail"]))
        workflow_rows.append(
            {
                "workflow_id": workflow_id,
                "ready": bool(host_ready and envs_ready and snakemake_env_ok),
                "command_envs": command_envs,
                "snakemake_prewarm_ready": snakemake_ready,
                "snakemake_prewarm_input_gated": snakemake_input_gated,
                "detail": "; ".join(detail_parts),
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "host_env_ready": host_ready,
        "special_envs": sorted(special_env_status.values(), key=lambda x: x["env_name"]),
        "special_env_ready_count": sum(1 for row in special_env_status.values() if row["ready"]),
        "workflow_readiness": workflow_rows,
        "snakemake_prewarm_ready_count": sum(1 for row in workflow_rows if row["snakemake_prewarm_ready"]),
        "excluded_command_envs": sorted(excluded_envs),
    }
    write_status_report(payload)
    print(SANDBOX_STATUS_JSON)
    print(SANDBOX_STATUS_MD)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
