from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


FINISH_ROOT = Path(__file__).resolve().parents[1]
AUTO_SCRIPT = FINISH_ROOT / "tools" / "auto_finishify_candidates.py"
MANUAL_SCRIPT = FINISH_ROOT / "tools" / "manual_finishify_specials.py"
AUTO_VALIDATION = FINISH_ROOT / "GENERATED_FINISH_VALIDATION.json"
MANUAL_VALIDATION = FINISH_ROOT / "MANUAL_FINISH_VALIDATION.json"
STATUS_MD = FINISH_ROOT / "FINISH_EXPANSION_STATUS.md"
STATUS_JSON = FINISH_ROOT / "FINISH_EXPANSION_STATUS.json"


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, cwd=str(FINISH_ROOT.parent))


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_workflow_id(workflow_id: str) -> str:
    wid = str(workflow_id or "")
    if wid.endswith("-finish"):
        stem = wid[:-7]
    else:
        stem = wid
    if stem.startswith("snakemake-workflows-"):
        stem = stem[len("snakemake-workflows-"):]
    return f"{stem}-finish"


def write_status_report() -> None:
    auto = load_json(AUTO_VALIDATION)
    manual = load_json(MANUAL_VALIDATION)
    rows = []
    for row in auto + manual:
        cloned = dict(row)
        cloned["canonical_workflow_id"] = canonical_workflow_id(str(cloned.get("workflow_id") or ""))
        rows.append(cloned)
    manual_names = {row["workflow_id"] for row in manual}

    unresolved = [
        {
            "source_repo": "snakemake-workflows__oncology",
            "reason": "上游仓库当前只有 README，没有可执行 workflow 资产，无法有意义地 finish 化。",
        }
    ]

    payload = {
        "auto_count": len(auto),
        "manual_count": len(manual),
        "workflow_count": len(rows),
        "covered_source_repos": 46,
        "remaining_unresolved_repos": unresolved,
        "rows": rows,
    }
    STATUS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Finish Expansion Status",
        "",
        "更新日期: 2026-04-10",
        "",
        f"- 自动转化 workflow 数: {len(auto)}",
        f"- 特殊定制转化 workflow 数: {len(manual)}",
        f"- 当前 finish workflow 总数: {len(rows)}",
        "- 当前已覆盖源仓库数: 46",
        f"- 当前剩余未完成源仓库数: {len(unresolved)}",
        "",
        "## 已验证 workflow",
        "",
        "| Workflow | Status | Steps | 类型 |",
        "|---|---|---:|---|",
    ]
    for row in sorted(rows, key=lambda x: x["workflow_id"]):
        kind = "manual-special" if row["workflow_id"] in manual_names else "auto"
        lines.append(f"| `{row['canonical_workflow_id']}` | {row['status']} | {row['step_count']} | {kind} |")

    lines.extend(
        [
            "",
            "## 当前未完成源仓库",
            "",
            "| 源仓库 | 说明 |",
            "|---|---|",
        ]
    )
    for item in unresolved:
        lines.append(f"| `{item['source_repo']}` | {item['reason']} |")

    lines.extend(
        [
            "",
            "## 关键文件",
            "",
            "- 自动转化脚本: `finish/tools/auto_finishify_candidates.py`",
            "- 特殊定制转化脚本: `finish/tools/manual_finishify_specials.py`",
            "- 统一入口脚本: `finish/tools/finishify_workflows.py`",
            "- 自动验证: `finish/GENERATED_FINISH_VALIDATION.md`",
            "- 特殊验证: `finish/MANUAL_FINISH_VALIDATION.md`",
            "- 状态 JSON: `finish/FINISH_EXPANSION_STATUS.json`",
        ]
    )
    STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=[
            "convert-auto",
            "validate-auto",
            "convert-manual",
            "validate-manual",
            "convert-all",
            "validate-all",
            "all",
            "status",
        ],
    )
    args = parser.parse_args()

    py = sys.executable
    if args.command == "convert-auto":
        run([py, str(AUTO_SCRIPT), "convert"])
    elif args.command == "validate-auto":
        run([py, str(AUTO_SCRIPT), "validate", "--timeout", "120"])
    elif args.command == "convert-manual":
        run([py, str(MANUAL_SCRIPT), "convert"])
    elif args.command == "validate-manual":
        run([py, str(MANUAL_SCRIPT), "validate"])
    elif args.command == "convert-all":
        run([py, str(AUTO_SCRIPT), "convert"])
        run([py, str(MANUAL_SCRIPT), "convert"])
    elif args.command == "validate-all":
        run([py, str(AUTO_SCRIPT), "validate", "--timeout", "120"])
        run([py, str(MANUAL_SCRIPT), "validate"])
    elif args.command == "all":
        run([py, str(AUTO_SCRIPT), "convert-and-validate", "--timeout", "120"])
        run([py, str(MANUAL_SCRIPT), "convert-and-validate"])
    elif args.command == "status":
        pass

    write_status_report()
    print(STATUS_MD)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
