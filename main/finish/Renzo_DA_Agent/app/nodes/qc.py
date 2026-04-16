"""qc node — runs the QC rule chain on execution outputs.

Routing decisions:
  - All rules pass (or only warnings) -> step_finalize  (proceed)
  - Any rule fails                     -> planner       (replan)
  - Review needed (warn with review)   -> hitl           (ask human)

Special case – step5_qc_and_final_report:
  Step 5 must never fail.  Regardless of QC results the node always
  routes to step_finalize with status downgraded to "warn" so the
  responder generates a report describing whatever QC situation exists.
"""
from __future__ import annotations

import logging
import os
from typing import Dict

from renzo.app.state import AgentState
from renzo.app.validators.rules import run_qc_rules, summarize_qc
from renzo.app.experiments import resolve_execution_workdir

logger = logging.getLogger(__name__)


def qc_node(state: AgentState) -> Dict:
    """Run QC rule chain and decide whether to proceed, replan, or ask human."""
    logs = state.get("execution_logs", [])
    latest_log = logs[-1] if logs else {}

    outputs_dir = state.get("execution_workdir") or str(
        resolve_execution_workdir(
            state.get("experiment_id"),
            state.get("session_id"),
            state.get("artifact_policy", "session"),
        )
    )

    # Build context for rules
    ctx = {
        "latest_log": latest_log,
        "outputs_dir": outputs_dir,
        "data_profile": state.get("data_profile", {}),
        "data_catalog": state.get("data_catalog", []),
    }

    # Run all QC rules
    rule_results = run_qc_rules(ctx)
    summary = summarize_qc(rule_results)

    # Append to qc_results history
    qc_history = list(state.get("qc_results", []))
    qc_history.append(summary)

    # ── Step 5 override: never fail, always finalize ─────────────────
    _cur_step = state.get("current_step_id") or ""
    if _cur_step == "step5_qc_and_final_report":
        if summary["status"] == "fail":
            logger.warning(
                "Step5 QC returned 'fail' — downgrading to 'warn' so report is generated."
            )
            summary["status"] = "warn"
        return {
            "qc_results": qc_history,
            "validation_result": summary,
            "next_node": "step_finalize",
        }

    # ── Normal routing for other steps ───────────────────────────────
    if summary["status"] == "fail":
        run_ctx = dict(state.get("workflow_run_context") or {})
        strict_manifest = bool(run_ctx.get("strict_manifest", False))
        if state.get("workflow_plan") and strict_manifest:
            return {
                "qc_results": qc_history,
                "validation_result": summary,
                "workflow_status": "failed",
                "next_node": "step_finalize",
            }
        return {
            "qc_results": qc_history,
            "validation_result": summary,
            "next_node": "planner",
        }

    needs_review = [r for r in rule_results if r.get("needs_review", False)]
    if needs_review:
        review_details = "\n".join(
            f"- {r.get('rule', 'Unknown')}: {r.get('message', 'No details')}"
            for r in needs_review
        )
        return {
            "qc_results": qc_history,
            "validation_result": summary,
            "hitl_pending": True,
            "hitl_question": "QC validation found issues that need your review. Should we proceed or replan?",
            "hitl_context": f"QC Results:\n{review_details}",
            "hitl_reason": "Some QC checks produced warnings that may need human judgment.",
            "hitl_origin_node": "qc",
            "next_node": "hitl",
        }

    return {
        "qc_results": qc_history,
        "validation_result": summary,
        "next_node": "step_finalize",
    }
