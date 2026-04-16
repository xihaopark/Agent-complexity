from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


FINISH_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_CANDIDATES = FINISH_ROOT / "workflow_candidates"
VALIDATION_JSON = FINISH_ROOT / "GENERATED_FINISH_VALIDATION.json"
VALIDATION_MD = FINISH_ROOT / "GENERATED_FINISH_VALIDATION.md"

RULE_RE = re.compile(r"^\s*(?:rule|checkpoint)\s+([A-Za-z0-9_.-]+)\s*:")
INCLUDE_RE = re.compile(r"^\s*include\s*:\s*(.+?)\s*$")
CONFIGFILE_RE = re.compile(r"^\s*configfile\s*:\s*(.+?)\s*$")

PREFERRED_SNAKEFILES = (
    "workflow/Snakefile",
    "Snakefile",
    "snakefile",
    "workflow/snakefile",
)
PREFERRED_CONFIGS = (
    ".test/config/config.yaml",
    ".test/config/config.yml",
    "config/config.yaml",
    "config/config.yml",
    "configs/config.yaml",
    "configs/config.yml",
    "config.yaml",
    "config.yml",
)


@dataclass
class CandidateInfo:
    repo_dir: Path
    snakefile: Path
    configfile: Path | None
    sample_hints: list[Path]
    rule_order: list[str]


def slugify(text: str) -> str:
    value = text.lower().replace("__", "-")
    return re.sub(r"[^a-z0-9._-]+", "-", value).strip("-._")


def canonical_repo_name(repo_name: str) -> str:
    value = repo_name
    for prefix in ("snakemake-workflows__", "snakemake-workflows-"):
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    return value


def finish_dir_name(repo_name: str) -> str:
    return f"{slugify(canonical_repo_name(repo_name))}-finish"


def workflow_owned_by_source(finish_dir: Path, source_repo_name: str) -> bool:
    metadata_path = finish_dir / "source-metadata.json"
    if not metadata_path.exists():
        return False
    try:
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    except Exception:
        return False
    existing = Path(str(payload.get("source_repo_dir") or "")).name
    return existing == source_repo_name


def iter_candidate_dirs(limit: int | None = None, only: set[str] | None = None) -> list[Path]:
    repos = []
    for repo_dir in sorted(WORKFLOW_CANDIDATES.iterdir()):
        if not repo_dir.is_dir() or repo_dir.name.startswith("_"):
            continue
        if only and repo_dir.name not in only:
            continue
        repos.append(repo_dir)
    if limit is not None:
        repos = repos[:limit]
    return repos


def detect_snakefile(repo_dir: Path) -> Path | None:
    for rel in PREFERRED_SNAKEFILES:
        path = repo_dir / rel
        if path.exists():
            return path
    candidates = sorted(
        path
        for path in repo_dir.rglob("*")
        if path.is_file() and path.name in {"Snakefile", "snakefile"}
    )
    return candidates[0] if candidates else None


def extract_path_expr(raw: str) -> str | None:
    text = raw.strip()
    if not text:
        return None
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        return text[1:-1]
    if text.startswith("os.path.join(") and text.endswith(")"):
        parts = re.findall(r"[\"']([^\"']+)[\"']", text)
        if parts:
            return "/".join(parts)
    return None


def resolve_expr_path(base_file: Path, raw: str) -> Path | None:
    text = raw.strip()
    suffix = extract_path_expr(text)
    candidates: list[Path] = []
    if suffix:
        candidates.append((base_file.parent / suffix).resolve())
    if suffix and "workflow.basedir" in text:
        candidates.append((base_file.parent / suffix).resolve())
    if suffix and "maindir" in text:
        for ancestor in base_file.resolve().parents:
            candidates.append((ancestor / suffix).resolve())
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists():
            return candidate
    return None


def parse_configfiles_from_sources(paths: Iterable[Path]) -> list[str]:
    found: list[str] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in text.splitlines():
            match = CONFIGFILE_RE.match(line)
            if match:
                resolved = resolve_expr_path(path, match.group(1))
                if resolved is not None:
                    found.append(str(resolved))
                    continue
                rendered = extract_path_expr(match.group(1))
                if rendered:
                    found.append(rendered)
    return found


def resolve_candidate_path(base_file: Path, raw: str) -> Path | None:
    rel = raw.strip()
    if not rel:
        return None
    candidate = (base_file.parent / rel).resolve()
    if candidate.exists():
        return candidate
    return None


def collect_include_graph(entry: Path) -> list[Path]:
    ordered: list[Path] = []
    seen: set[Path] = set()

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in seen or not path.exists():
            return
        seen.add(path)
        ordered.append(path)
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return
        for line in text.splitlines():
            match = INCLUDE_RE.match(line)
            if not match:
                continue
            candidate = resolve_expr_path(path, match.group(1))
            if candidate is None:
                rendered = extract_path_expr(match.group(1))
                if not rendered:
                    continue
                candidate = resolve_candidate_path(path, rendered)
            if candidate is not None:
                visit(candidate)

    visit(entry)
    return ordered


def parse_rules_in_order(paths: Iterable[Path]) -> list[str]:
    rules: list[str] = []
    seen: set[str] = set()
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for line in text.splitlines():
            match = RULE_RE.match(line)
            if not match:
                continue
            rule = match.group(1)
            if rule in seen:
                continue
            seen.add(rule)
            rules.append(rule)
    if "all" in seen:
        rules = [rule for rule in rules if rule != "all"] + ["all"]
    return rules


def detect_configfile(repo_dir: Path, source_files: list[Path]) -> Path | None:
    for path in source_files:
        for raw in parse_configfiles_from_sources([path]):
            resolved = resolve_candidate_path(path, raw)
            if resolved is not None and resolved.exists():
                return resolved
    for rel in PREFERRED_CONFIGS:
        path = repo_dir / rel
        if path.exists():
            return path
    yaml_candidates = sorted(
        path
        for path in repo_dir.rglob("*")
        if path.is_file() and path.suffix in {".yaml", ".yml"} and "env" not in path.parts and ".snakemake" not in path.parts
    )
    return yaml_candidates[0] if yaml_candidates else None


def detect_sample_hints(repo_dir: Path) -> list[Path]:
    hints: list[Path] = []
    for path in sorted(repo_dir.rglob("*")):
        if not path.is_file():
            continue
        name = path.name.lower()
        if name.startswith("samples") or name.startswith("units") or "targets" in name:
            if path.suffix.lower() in {".tsv", ".csv", ".txt"}:
                hints.append(path)
    return hints[:8]


def fallback_rule_list_with_snakemake(repo_dir: Path, snakefile: Path, configfile: Path | None) -> list[str]:
    command = [sys.executable, "-m", "snakemake", "-s", str(snakefile), "--list-rules"]
    if configfile is not None:
        command.extend(["--configfile", str(configfile)])
    try:
        completed = subprocess.run(
            command,
            cwd=str(repo_dir),
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except Exception:
        return []
    if completed.returncode != 0:
        return []
    rules: list[str] = []
    for line in completed.stdout.splitlines():
        text = line.strip()
        if not text or text.startswith("localrules:"):
            continue
        rules.append(text)
    if "all" in rules:
        rules = [rule for rule in rules if rule != "all"] + ["all"]
    seen: set[str] = set()
    deduped: list[str] = []
    for rule in rules:
        if rule in seen:
            continue
        seen.add(rule)
        deduped.append(rule)
    return deduped


def inspect_candidate(repo_dir: Path) -> CandidateInfo | None:
    snakefile = detect_snakefile(repo_dir)
    if snakefile is None:
        return None
    source_files = collect_include_graph(snakefile)
    configfile = detect_configfile(repo_dir, source_files)
    rule_order = parse_rules_in_order(source_files)
    if len(rule_order) < 2:
        fallback = fallback_rule_list_with_snakemake(repo_dir, snakefile, configfile)
        if fallback:
            rule_order = fallback
    rule_order = [rule for rule in rule_order if rule]
    if not rule_order:
        return None
    return CandidateInfo(
        repo_dir=repo_dir,
        snakefile=snakefile,
        configfile=configfile,
        sample_hints=detect_sample_hints(repo_dir),
        rule_order=rule_order,
    )


def rel_from_finish(path: Path) -> str:
    return str(path.resolve().relative_to(FINISH_ROOT.parent.resolve())).replace("\\", "/")


def source_rel_from_generated(repo_dir: Path, item: Path) -> str:
    rel = item.resolve().relative_to(FINISH_ROOT.resolve())
    return f"../{str(rel).replace(os.sep, '/')}"


def source_runtime_path(item: Path) -> str:
    return str(item.resolve())


def generate_common_smk(dest: Path) -> None:
    content = """from pathlib import Path
import shlex
import subprocess
import sys
import os


def _runtime_helper():
  root = os.environ.get("RENZO_RUNTIME_ROOT", "").strip()
  if root:
    path = (Path(root) / "app" / "finish_step_runtime.py").resolve()
    if path.exists():
      return path
  candidate = (Path(".").resolve().parent / "Renzo_DA_Agent" / "app" / "finish_step_runtime.py").resolve()
  return candidate if candidate.exists() else None


def ensure_paths(paths):
  for path in paths:
    resolved = (Path(".") / path).resolve()
    if not resolved.exists():
      raise FileNotFoundError(f"Missing required path: {path}")


def write_stamp(output_path, step_id, command):
  output_path = Path(output_path)
  output_path.parent.mkdir(parents=True, exist_ok=True)
  output_path.write_text(f"{step_id}\\n{command}\\n", encoding="utf-8")


def run_step(step_id, output_path):
  helper = _runtime_helper()
  if helper is not None:
    subprocess.run(
      [
        sys.executable,
        str(helper),
        "--config-file",
        "config_basic/config.yaml",
        "--step-id",
        step_id,
        "--output-path",
        str(output_path),
      ],
      check=True,
    )
    return

  step = config["steps"][step_id]
  ensure_paths(step.get("requires", []))
  command = step.get("command", "").format(source_cores=config.get("source_cores", 8))
  if command:
    command_parts = shlex.split(command)
    if command_parts and command_parts[0] == "snakemake":
      command_parts = [sys.executable, "-m", "snakemake", *command_parts[1:]]
    subprocess.run(command_parts, check=True)
  write_stamp(output_path, step_id, command)
"""
    dest.write_text(content, encoding="utf-8")


def generate_step_wrapper(dest: Path, step_id: str) -> None:
    content = f"""configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "{step_id}"


rule all:
  input:
    "results/finish/{step_id}.done"


rule run_{step_id.replace('-', '_').replace('.', '_')}:
  output:
    "results/finish/{step_id}.done"
  run:
    run_step(STEP_ID, output[0])
"""
    dest.write_text(content, encoding="utf-8")


def generate_run_workflow(dest: Path, steps: list[str]) -> None:
    content = f"""from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STEPS = {json.dumps(steps, ensure_ascii=False)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cores", default="8")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--from-step")
    parser.add_argument("--to-step")
    return parser.parse_args()


def pick_steps(start: str | None, end: str | None) -> list[str]:
    start_index = STEPS.index(start) if start else 0
    end_index = STEPS.index(end) + 1 if end else len(STEPS)
    if start_index >= end_index:
        raise ValueError("from-step must be earlier than or equal to to-step")
    return STEPS[start_index:end_index]


def main() -> int:
    args = parse_args()
    for step_id in pick_steps(args.from_step, args.to_step):
        command = [
            sys.executable,
            "-m",
            "snakemake",
            "-s",
            f"steps/{{step_id}}.smk",
            "--configfile",
            "config_basic/config.yaml",
            "--cores",
            args.cores,
        ]
        if args.dry_run:
            command.append("-n")
        print(f"== {{step_id}} ==")
        print(" ".join(command))
        proc = subprocess.run(command, cwd=ROOT)
        if proc.returncode != 0:
            return proc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""
    dest.write_text(content, encoding="utf-8")


def generate_agent_steps_md(dest: Path, workflow_id: str, info: CandidateInfo) -> None:
    lines = [
        f"# {workflow_id} LLM Execution Spec",
        "",
        "## Purpose",
        "",
        f"- Source repository: `{info.repo_dir.name}`",
        f"- Source snakefile: `{source_rel_from_generated(info.repo_dir, info.snakefile)}`",
        "- This generated finish workflow exposes the source workflow as stepwise checkpoints.",
        "- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.",
        "",
        "## Operating Rules",
        "",
        "- Execute steps in listed order.",
        "- Treat the source workflow as the implementation source of truth.",
        "- Do not mutate the source workflow structure during execution.",
        "- Stop on failure and report the exact source rule that could not be reached.",
        "",
        "## Step Order",
        "",
    ]
    for index, step_id in enumerate(info.rule_order, start=1):
        lines.append(f"{index}. `{step_id}`")
    lines.append("")
    dest.write_text("\n".join(lines), encoding="utf-8")


def build_step_config(step_id: str, prev_step: str | None, info: CandidateInfo) -> dict:
    source_snakefile = source_runtime_path(info.snakefile)
    step: dict[str, object] = {
        "summary": step_id,
        "requires": [],
        "snakemake": {
            "snakefile": source_snakefile,
            "directory": source_runtime_path(info.repo_dir),
            "use_conda": True,
            "cores": "{source_cores}",
            "scheduler": "greedy",
        },
    }
    if info.configfile is not None:
        step["requires"] = [source_runtime_path(info.configfile)]
        step["snakemake"]["configfile"] = source_runtime_path(info.configfile)
    nested = step["snakemake"]
    if step_id == "all":
        nested["targets"] = ["all"]
    else:
        nested["root_target"] = "all"
        nested["until"] = [step_id]
    if prev_step is not None:
        step["depends_on"] = [prev_step]
    return step


def build_manifest(workflow_id: str, finish_dir: Path, info: CandidateInfo) -> dict:
    steps = []
    prev_step: str | None = None
    for step_id in info.rule_order:
        step_entry = {
            "id": step_id,
            "name": step_id.replace("_", " ").replace("-", " "),
            "targets": ["all"] if step_id == "all" else [step_id],
            "params": {
                "snakefile": f"steps/{step_id}.smk",
                "configfile": "config_basic/config.yaml",
                "cores": 1,
                "run_directory": ".",
                "use_conda": False,
                "shared_conda_env": "snakemake",
            },
            "outputs": [f"results/finish/{step_id}.done"],
            "depends_on": [prev_step] if prev_step else [],
        }
        steps.append(step_entry)
        prev_step = step_id

    aliases = [finish_dir.name.replace("-finish", ""), workflow_id.replace("-finish", "")]
    input_hints = []
    if info.configfile is not None:
        input_hints.append(source_rel_from_generated(info.repo_dir, info.configfile))
    input_hints.extend(source_rel_from_generated(info.repo_dir, path) for path in info.sample_hints[:6])

    return {
        "id": workflow_id,
        "name": workflow_id.replace("-", " "),
        "engine": "snakemake",
        "entry_point": "run_workflow.py",
        "description": f"Auto-generated finish workflow for source repository {info.repo_dir.name}, split into source Snakemake rules as sequential checkpoints.",
        "version": "0.1",
        "aliases": aliases,
        "tags": ["finish", "autogenerated", "snakemake", "r-workflow", "candidate"],
        "url": f"https://github.com/{info.repo_dir.name.replace('__', '/')}",
        "know_how": "workflow/agent-steps.md",
        "know_how_files": ["workflow/agent-steps.md"],
        "discovery": {
            "kind": "finish_workflow",
            "family": "candidate",
            "aliases": aliases,
            "retained_steps": info.rule_order,
            "supports_partial_run": True,
            "runner": "python3 run_workflow.py --cores 8",
            "standard_step_skills": False,
            "generated_by": "tools/auto_finishify_candidates.py",
            "split_mode": "rule_until",
            "source_repo": info.repo_dir.name,
            "source_snakefile": source_rel_from_generated(info.repo_dir, info.snakefile),
        },
        "input_hints": input_hints,
        "output_hints": ["results/finish/*.done"],
        "steps": steps,
    }


def convert_candidate(info: CandidateInfo, overwrite: bool = True) -> Path:
    finish_dir = FINISH_ROOT / finish_dir_name(info.repo_dir.name)
    if finish_dir.exists() and overwrite:
        if not workflow_owned_by_source(finish_dir, info.repo_dir.name):
            raise RuntimeError(
                f"Refusing to overwrite existing workflow {finish_dir.name}; it is already reserved by another source workflow."
            )
        shutil.rmtree(finish_dir)
    finish_dir.mkdir(parents=True, exist_ok=True)
    (finish_dir / "config_basic").mkdir(exist_ok=True)
    (finish_dir / "results" / "finish").mkdir(parents=True, exist_ok=True)
    (finish_dir / "steps").mkdir(exist_ok=True)
    (finish_dir / "workflow").mkdir(exist_ok=True)

    config_data = {
        "workflow_id": finish_dir.name.replace("/", "-"),
        "source_cores": 8,
        "steps": {},
    }
    prev_step: str | None = None
    for step_id in info.rule_order:
        config_data["steps"][step_id] = build_step_config(step_id, prev_step, info)
        prev_step = step_id
        generate_step_wrapper(finish_dir / "steps" / f"{step_id}.smk", step_id)

    generate_common_smk(finish_dir / "steps" / "common.smk")
    generate_run_workflow(finish_dir / "run_workflow.py", info.rule_order)
    generate_agent_steps_md(
        finish_dir / "workflow" / "agent-steps.md",
        finish_dir.name,
        info,
    )

    (finish_dir / "config_basic" / "config.yaml").write_text(
        yaml.safe_dump(config_data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    manifest = build_manifest(finish_dir.name, finish_dir, info)
    (finish_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (finish_dir / "source-metadata.json").write_text(
        json.dumps(
            {
                "source_repo_dir": str(info.repo_dir),
                "source_snakefile": str(info.snakefile),
                "source_configfile": str(info.configfile) if info.configfile else None,
                "step_count": len(info.rule_order),
                "steps": info.rule_order,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return finish_dir


def validate_generated_workflow(finish_dir: Path, timeout_seconds: int = 180) -> dict:
    manifest = json.loads((finish_dir / "manifest.json").read_text(encoding="utf-8"))
    steps = [step["id"] for step in manifest.get("steps", [])]
    command = [sys.executable, "run_workflow.py", "--dry-run", "--cores", "1"]
    try:
        completed = subprocess.run(
            command,
            cwd=str(finish_dir),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        return {
            "workflow_id": manifest.get("id", finish_dir.name),
            "workflow_dir": str(finish_dir),
            "step_count": len(steps),
            "status": "passed" if completed.returncode == 0 else "failed",
            "returncode": completed.returncode,
            "stdout_tail": "\n".join(completed.stdout.splitlines()[-20:]),
            "stderr_tail": "\n".join(completed.stderr.splitlines()[-20:]),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "workflow_id": manifest.get("id", finish_dir.name),
            "workflow_dir": str(finish_dir),
            "step_count": len(steps),
            "status": "timeout",
            "returncode": None,
            "stdout_tail": "\n".join((exc.stdout or "").splitlines()[-20:]),
            "stderr_tail": "\n".join((exc.stderr or "").splitlines()[-20:]),
        }


def write_validation_reports(results: list[dict]) -> None:
    VALIDATION_JSON.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# Generated Finish Validation",
        "",
        f"- Total workflows validated: {len(results)}",
        f"- Passed: {sum(1 for row in results if row['status'] == 'passed')}",
        f"- Failed: {sum(1 for row in results if row['status'] == 'failed')}",
        f"- Timeout: {sum(1 for row in results if row['status'] == 'timeout')}",
        "",
        "| Workflow | Status | Steps | Return Code |",
        "|---|---|---:|---:|",
    ]
    for row in results:
        lines.append(
            f"| `{row['workflow_id']}` | {row['status']} | {row['step_count']} | {row['returncode'] if row['returncode'] is not None else ''} |"
        )
    VALIDATION_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["convert", "validate", "convert-and-validate"])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    only = set(args.only or [])
    repos = iter_candidate_dirs(limit=args.limit, only=only or None)
    converted: list[Path] = []
    skipped: list[dict] = []

    if args.command in {"convert", "convert-and-validate"}:
        for repo_dir in repos:
            info = inspect_candidate(repo_dir)
            if info is None:
                skipped.append({"repo": repo_dir.name, "reason": "no_supported_snakemake_entry"})
                continue
            finish_dir = FINISH_ROOT / finish_dir_name(repo_dir.name)
            if finish_dir.exists() and not workflow_owned_by_source(finish_dir, repo_dir.name) and args.skip_existing:
                skipped.append({"repo": repo_dir.name, "reason": f"canonical_name_reserved_by_existing:{finish_dir.name}"})
                continue
            if finish_dir.exists() and args.skip_existing:
                converted.append(finish_dir)
                continue
            try:
                converted.append(convert_candidate(info))
            except RuntimeError as exc:
                skipped.append({"repo": repo_dir.name, "reason": str(exc)})
        print(json.dumps({"converted": [path.name for path in converted], "skipped": skipped}, indent=2, ensure_ascii=False))

    if args.command in {"validate", "convert-and-validate"}:
        if not converted:
            for repo_dir in repos:
                finish_dir = FINISH_ROOT / finish_dir_name(repo_dir.name)
                if finish_dir.exists():
                    converted.append(finish_dir)
        results = [validate_generated_workflow(path, timeout_seconds=args.timeout) for path in converted if path.exists()]
        write_validation_reports(results)
        print(json.dumps({"validation_results": results[:5], "report_json": str(VALIDATION_JSON), "report_md": str(VALIDATION_MD)}, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
