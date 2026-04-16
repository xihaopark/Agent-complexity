"""responder node -- generates a natural, context-aware user-facing summary.

This is the final node before END.  It:
  1. Gathers the goal, plan, execution results, QC summary, and artifacts.
  2. Calls the LLM to produce a **natural** Markdown response (not a fixed template).
  3. Collects artifacts produced in the *current* step as structured attachments
     so the frontend can render them inline in the chat message.
  4. Sets terminate=True.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from renzo.app.state import AgentState
from renzo.app.llm import get_llm
from renzo.app.tracing import append_trace, build_llm_trace_entry

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt -- natural, adaptive style
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are **Renzo**, a data-analysis assistant.  Write naturally as a \
knowledgeable analyst sharing findings with a colleague -- not as a bot \
filling in a template.

IMPORTANT: Always respond in English regardless of the user's input language.

Tone and language:
- Reply in a **human, conversational way** — natural and flexible; vary your phrasing. Do not follow a fixed template.
- Use **simple, plain language**. Use **line breaks and short paragraphs** so the reply is easy to scan; avoid one long block of text.
- Use **symbols** where they help: • for bullets, — for emphasis, ✓/✗ for pass/fail when listing items. You may use **light emoji** occasionally (e.g. 👍 ✅ 📋) to add tone, but sparingly — not every sentence.
- Use a warm, lively tone; *you* and *we* are fine. Explain technical terms briefly in plain words when needed.

Reply structure:
- Keep the reply **short**: 2–4 sentences or a few bullets. Use **multiple line breaks** between ideas. Include only what directly answers the goal.
- **End with one or two short suggestions**: what to do next (e.g. say **continue**, or share X). One line is enough.

Reply style:
- Only show content directly relevant to the user's question.
- For **statistics, file lists, data summaries** use **Markdown tables** (| Col1 | Col2 |). Prefer tables over long bullet lists for data.
- When describing steps, use **bold** and clear headings; use • or — to break up text.

CRITICAL — Match the user's goal:
- If the user asked for **dataset details**, **check datasets**, **inventory**, or **what files/data we have**: lead with the **files and datasets** (names, row/column counts, domains). Mention QC only briefly at the end if at all. Do NOT lead with QC findings.
- If the user asked for **profile**, **statistics**, or **summary of the data**: lead with concrete numbers and file list; briefly list each output (one line each).
- If the user asked for **validation** or **QC**: give a **one- or two-sentence summary only** (e.g. "QC passed" or "X checks failed — see the table below"). Do NOT write a long paragraph describing each QC item; a table is shown separately below your reply.
- List every output file/table/artifact produced **briefly** (e.g. "dm.csv: 254 rows × 45 columns"). Never say only "CSV read successfully" when there are named outputs — name them.

Guidelines:
- Lead with what the user asked for. Use line breaks and symbols (• — ✓ ✗) to keep the reply scannable.
- When a CSV/table was produced, quote specific numbers or patterns; you may include small Markdown tables.
- When a plot/image was produced, describe what it shows and mention the filename.
- Adapt length: data-loading -> concise list + key stats; analytical step -> highlights + outputs; error -> what went wrong and next step.
- If there are remaining pending steps, your closing suggestion can be e.g. "Reply **continue** or give new instructions." Omit when all steps are done.
- Write in flowing prose with Markdown where helpful. Avoid rigid "1. What was completed" sections.

CRITICAL — No code blocks:
- Do NOT include raw code or markdown code blocks (triple-backtick fences) in your reply. Describe results in plain language; code and long run output are shown elsewhere.
"""


# ---------------------------------------------------------------------------
# Helpers: strip code blocks so restored output never shows raw code in chat
# ---------------------------------------------------------------------------

def _strip_markdown_code_blocks(text: str) -> str:
    """Remove markdown code fences (```...```) from text. Replaces each block with a short placeholder."""
    if not text or not isinstance(text, str):
        return text
    # Match ```optional_lang\n...\n``` (non-greedy)
    return re.sub(r"```[\w{}\s]*\n.*?```", "(output omitted)", text, flags=re.DOTALL).strip()


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

def responder_node(state: AgentState) -> Dict:
    """Generate a user-facing summary and terminate the run."""
    goal = state.get("goal", "Analyze data")
    answer_only_goal = state.get("answer_only_goal", "").strip()
    llm_trace = list(state.get("llm_trace") or [])

    # ── Answer-only path: direct reply without execution ─────────────
    if answer_only_goal:
        messages = state.get("messages") or []
        suggested_mode = state.get("suggested_mode") or ""
        if suggested_mode:
            summary = (
                "This request would be better handled with a full analysis (code and execution). "
                f"**Switch to {suggested_mode.capitalize()} mode** to run a plan and generate outputs. If you switch, I can run the full analysis."
            )
        else:
            summary, llm_entry = _generate_answer_only_reply(answer_only_goal, messages, state)
            llm_trace = append_trace(llm_trace, llm_entry)
            if not summary:
                summary = _fallback_answer_only(answer_only_goal, messages)
        if summary:
            summary = _strip_markdown_code_blocks(summary)
        return {
            "messages": [AIMessage(content=summary or "")],
            "response_attachments": [],
            "llm_trace": llm_trace,
            "terminate": True,
            "answer_only_goal": "",
            "suggested_mode": suggested_mode or None,
        }

    plan_steps = state.get("plan_steps", [])
    execution_logs = state.get("execution_logs", [])
    qc_results = state.get("qc_results", [])
    artifact_index: List[Dict[str, Any]] = state.get("artifact_index", [])
    plan_status = state.get("plan_status", "unknown")
    current_step_id = state.get("current_step_id", "")
    workflow_plan = state.get("workflow_plan")
    workflow_status = state.get("workflow_status", "")

    # ── Build context for the LLM ─────────────────────────────────────

    # Execution logs (latest runs)
    logs_summary = []
    for log in execution_logs[-5:]:
        logs_summary.append({
            "run_id": log.get("run_id", ""),
            "status": log.get("status", ""),
            "stdout_excerpt": log.get("stdout", "")[:2000],
            "stderr_excerpt": log.get("stderr", "")[:500],
        })

    latest_qc = qc_results[-1] if qc_results else {}

    # Artifact list -- include previews so LLM can cite real numbers
    artifacts_summary = []
    for art in artifact_index[:30]:
        entry: Dict[str, Any] = {
            "filename": art.get("filename", ""),
            "type": art.get("type", ""),
            "size_bytes": art.get("size_bytes", 0),
            "path": art.get("path", ""),
            "step_id": art.get("step_id", ""),
        }
        # Include preview data so the LLM can quote specific values
        preview = art.get("preview")
        if preview and isinstance(preview, str) and len(preview) < 3000:
            entry["preview_data"] = preview
        artifacts_summary.append(entry)

    # Workflow plan details
    wf_summary = ""
    if workflow_plan and isinstance(workflow_plan, dict):
        wf_steps = workflow_plan.get("steps", [])
        wf_lines = [f"Workflow: {workflow_plan.get('workflow_id', '?')} ({workflow_plan.get('status', '?')})"]
        for ws in wf_steps:
            wf_lines.append(f"  [{ws.get('status','?')}] {ws.get('id','?')}: {ws.get('description','')}")
        wf_summary = "\n".join(wf_lines)

    # Progress
    completed = [s for s in plan_steps if s.get("status") == "completed"]
    pending = [s for s in plan_steps if s.get("status") in ("pending", "in_progress")]
    failed = [s for s in plan_steps if s.get("status") == "failed"]
    total = len(plan_steps)
    done = len(completed)

    progress = f"Step progress: {done}/{total} completed"
    if failed:
        progress += f", {len(failed)} failed"
    if pending:
        progress += f", {len(pending)} remaining"

    # Current step info
    current_step_desc = ""
    for s in plan_steps:
        if s.get("id") == current_step_id:
            current_step_desc = s.get("description", current_step_id)
            break

    # Detect situation
    all_done = len(pending) == 0 and len(failed) == 0 and done > 0
    has_errors = len(failed) > 0 or any(
        log.get("status") == "error" for log in logs_summary
    )

    situation_hint = "intermediate_step"
    if all_done:
        situation_hint = "final_summary"
    elif has_errors:
        situation_hint = "error_recovery"
    elif done == 1 and total > 1:
        situation_hint = "first_step"

    plan_only_hint = ""
    if plan_status == "planned":
        plan_only_hint = (
            "The user only asked for a plan (no execution). Summarize the plan in **2–5 short bullet points or a very short table**. "
            "Do not list every detail; highlight key steps and outcomes only.\n\n"
        )
    qc_brief_hint = ""
    qc_details = latest_qc.get("details") if isinstance(latest_qc, dict) else []
    if qc_details:
        qc_brief_hint = (
            "IMPORTANT — QC results: A **table with check results (pass/fail/warn) is shown below your reply**. "
            "Do NOT write a long paragraph describing each QC item. In your reply, give only a one- or two-sentence summary (e.g. 'QC passed' or '2 checks failed — see the table below') and direct the user to the table.\n\n"
        )
    user_msg = (
        f"Goal (answer this directly): {goal}\n\n"
        f"{plan_only_hint}"
        f"{qc_brief_hint}"
        f"Structure your reply to address the goal above. If the goal is about dataset details/check/inventory, lead with files, domains, and key stats; list all outputs; mention QC only briefly. If the goal is about QC/validation, give a brief summary only; the table below your reply shows each check.\n\n"
        f"Current step: {current_step_desc} (id: {current_step_id})\n"
        f"Situation: {situation_hint}\n"
        f"{progress}\n\n"
        f"Plan steps:\n{json.dumps(plan_steps, indent=2, default=str)}\n\n"
        f"Workflow:\n{wf_summary}\n\n"
        f"Execution output (latest):\n"
        f"{json.dumps(logs_summary[-2:], indent=2, default=str)}\n\n"
        f"Output artifacts ({len(artifacts_summary)} files) — you MUST list each with a short description:\n"
        f"{json.dumps(artifacts_summary, indent=2, default=str)}\n\n"
        f"QC results (for context only; do not elaborate — table is shown separately):\n{json.dumps(latest_qc, indent=2, default=str)}\n\n"
        f"Write your response to the user. Use line breaks and symbols (• — ✓ ✗) where helpful; keep it short and conversational. End with 1–2 suggestions for next step or what would help."
    )

    # ── Generate ──────────────────────────────────────────────────────

    latest_stdout = ""
    if logs_summary:
        latest_stdout = logs_summary[-1].get("stdout_excerpt", "")

    summary, llm_entry = _generate_summary_via_llm(user_msg, state)
    llm_trace = append_trace(llm_trace, llm_entry)
    if not summary:
        summary = _fallback_summary(goal, plan_status, latest_stdout, artifacts_summary)
    if summary:
        summary = _strip_markdown_code_blocks(summary)

    # ── Collect current-step attachments for inline rendering ─────────
    current_step_artifacts = _collect_step_attachments(
        artifact_index, current_step_id
    )

    # ── QC table for frontend (green check / red cross in conversation) ──
    response_qc_table: Optional[List[Dict[str, Any]]] = None
    if isinstance(latest_qc, dict) and latest_qc.get("details"):
        response_qc_table = latest_qc["details"]

    out: Dict[str, Any] = {
        "messages": [AIMessage(content=summary or "")],
        "response_attachments": current_step_artifacts,
        "llm_trace": llm_trace,
        "terminate": True,
    }
    if response_qc_table is not None:
        out["response_qc_table"] = response_qc_table
    return out


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_ANSWER_ONLY_SYSTEM = """You are a helpful data-analysis assistant in **Ask mode** (like Cursor Ask): direct Q&A only — no code execution, no data loading.
- You **have access to the current session/run context** (experiment, plan steps with statuses, last run result, workflow status). Use it to answer questions like "anything wrong?", "can we move to next step?", or "what's the status?" — answer from the provided run context; do not say you cannot see it.
- Reply in a **human, conversational way** — natural and flexible. Use **line breaks and short paragraphs**; avoid one long block of text. You may use **symbols** (• — ✓ ✗) and occasional **light emoji** (e.g. 👍 ✅) where they fit; keep it scannable and lively.
- Be conversational and easy to understand; explain in simple language when needed. Keep the reply short: 2–4 sentences or a few bullets. Do not repeat the question or add filler.
- End with a short suggestion (what to try next or what would help). Lead with the direct answer. Do not say "I will load data" or "I will run code" — just answer.
- Do NOT include raw code or markdown code blocks (triple-backtick fences) in your reply.
- If the user has linked datasets or a workflow, reference them briefly when relevant. For how-to questions, give a practical overview in plain language. Write in English."""


def _last_user_content(messages: list) -> str:
    """Extract the last user message content for context."""
    for m in reversed(messages):
        kind = getattr(m, "type", None) or getattr(m, "role", "")
        if kind == "human" or (isinstance(m, dict) and m.get("role") == "user"):
            content = getattr(m, "content", None) or (m.get("content") if isinstance(m, dict) else "")
            if content:
                return (content[:1500] if isinstance(content, str) else str(content)[:1500])
    return ""


def _build_answer_only_session_context(state: Optional[Dict[str, Any]]) -> str:
    """Build a short session/run context string for Ask mode so the agent can answer status/next-step questions."""
    if not state:
        return ""
    lines: List[str] = []
    exp_id = state.get("experiment_id") or state.get("session_id")
    if exp_id:
        lines.append(f"Experiment/session: {exp_id}")
    plan_steps = state.get("plan_steps") or []
    if plan_steps:
        step_summaries = []
        for s in plan_steps[:20]:
            sid = s.get("id", "?")
            status = s.get("status", "?")
            desc = (s.get("description") or s.get("title") or sid)[:60]
            step_summaries.append(f"  {sid}: {status} — {desc}")
        lines.append("Plan steps (id: status — description):")
        lines.extend(step_summaries)
    logs = state.get("execution_logs") or []
    if logs:
        last = logs[-1]
        run_status = last.get("status", "unknown")
        lines.append(f"Last run status: {run_status}")
        if run_status not in ("success", "completed"):
            stderr = (last.get("stderr") or last.get("stderr_tail") or "")[:400]
            if stderr:
                lines.append("Last stderr excerpt: " + stderr.replace("\n", " ").strip())
    wp = state.get("workflow_plan") or {}
    if wp:
        wf_status = state.get("workflow_status") or wp.get("status", "?")
        current_step = state.get("current_step_id") or wp.get("current_step_id", "?")
        lines.append(f"Workflow status: {wf_status}; current step: {current_step}")
    plan_status = state.get("plan_status", "")
    if plan_status:
        lines.append(f"Plan status: {plan_status}")
    if not lines:
        return ""
    return "Current session/run context (use this to answer questions about run status, errors, or next step):\n" + "\n".join(lines)


def _generate_answer_only_reply(
    goal: str,
    messages: list,
    state: Optional[Dict[str, Any]] = None,
) -> tuple[Optional[str], Dict[str, Any]]:
    """Generate a short, focused answer for Ask mode (no execution). No link = simple Q&A; with link = can reference briefly."""
    prompt_messages = []
    llm = None
    try:
        llm = get_llm(temperature=0.3, max_tokens=1024)
        # Strip mode prefix so the LLM sees only the user question
        goal_clean = goal
        for prefix in ("[Mode: ask]\n\n", "[Mode: ask]\n", "[Mode: ask]"):
            if goal_clean.startswith(prefix):
                goal_clean = goal_clean[len(prefix):].strip()
                break
        recent = _last_user_content(messages)
        context = (
            ("Recent user message: " + recent + "\n\n") if recent else ""
        ) + "Current question (answer only, keep it short): " + goal_clean[:1500]
        linked_note = ""
        if state:
            ds_ctx = (state.get("dataset_context") or "").strip()
            wf_id = state.get("workflow_id_requested") or (state.get("workflow_plan") or {}).get("workflow_id")
            if ds_ctx or wf_id:
                parts = []
                if wf_id:
                    parts.append(f"linked workflow: {wf_id}")
                if ds_ctx:
                    parts.append("linked dataset(s) available")
                linked_note = "\nLinked context: " + "; ".join(parts) + ". Reference only if relevant; keep the answer concise.\n\n"
        session_context = _build_answer_only_session_context(state)
        session_block = ("\n\n" + session_context) if session_context else ""
        user_prompt = (
            "The user is in Ask mode (short Q&A only).\n\n"
            + linked_note
            + "Context:\n" + context
            + session_block
            + "\n\nProvide a brief, helpful answer in a natural, conversational way (2–4 sentences or short bullets). Use line breaks where helpful; avoid one big paragraph. If you used the session/run context above to answer (e.g. status or current step), you may start with a short line like 'Based on the current run: ...' so the user knows the answer is grounded in their session. End with one short suggestion for next step or what would help. Do not repeat the question or add filler; answer only what was asked."
        )
        prompt_messages = [
            SystemMessage(content=_ANSWER_ONLY_SYSTEM),
            HumanMessage(content=user_prompt),
        ]
        response = llm.invoke(prompt_messages)
        trace_context = {"goal": goal[:500]}
        if state:
            trace_context.update(
                {
                    "workflow_id": state.get("workflow_id_requested") or (state.get("workflow_plan") or {}).get("workflow_id"),
                    "current_step_id": state.get("current_step_id"),
                }
            )
        return response.content, build_llm_trace_entry(
            node="responder",
            purpose="answer_only_reply",
            prompt_messages=prompt_messages,
            response=response,
            status="success",
            parsed_output={"reply_length": len(str(response.content or ""))},
            context=trace_context,
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )
    except Exception as e:
        logger.error("Answer-only LLM failed: %s", e)
        trace_context = {"goal": goal[:500]}
        if state:
            trace_context.update(
                {
                    "workflow_id": state.get("workflow_id_requested") or (state.get("workflow_plan") or {}).get("workflow_id"),
                    "current_step_id": state.get("current_step_id"),
                }
            )
        return None, build_llm_trace_entry(
            node="responder",
            purpose="answer_only_reply",
            prompt_messages=prompt_messages,
            response=None,
            status="error",
            parsed_output=None,
            error=str(e),
            context=trace_context,
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )


def _fallback_answer_only(goal: str, messages: list) -> str:
    """Fallback when LLM is unavailable for answer-only."""
    combined = (goal + " " + _last_user_content(messages)).lower()
    if "sdtm" in combined and "adam" in combined:
        return (
            "**SDTM to ADaM (general overview)**\n\n"
            "- **ADSL** (subject-level): Derive from DM (demographics, treatment start/end, population flags). "
            "Key variables: USUBJID, TRT01P/TRT01A, TRTSDT/TRTEDT, SAFFL, etc.\n"
            "- **ADAE, ADLB, ADVS**: Occurrence (AE) and BDS (LB, VS) datasets; map from AE, LB, VS with "
            "analysis dates, baseline, change from baseline, visit/parameter coding.\n"
            "- **Typical steps**: (1) Define target ADaM datasets and specs, (2) Map SDTM domains and variables, "
            "(3) Apply derivation rules (treatment, flags, windows), (4) Validate (e.g. against define.xml / SAP).\n\n"
            "For your specific study, share which SDTM domains you have and which ADaM datasets you need, and I can outline the exact mappings."
        )
    return (
        f"I'm in answer-only mode (no code run). Your request: {goal[:200]}.\n\n"
        "Reply with a specific question if you want a short answer, or say **continue** to run a full analysis."
    )


def _generate_summary_via_llm(
    user_msg: str,
    state: Optional[Dict[str, Any]] = None,
) -> tuple[Optional[str], Dict[str, Any]]:
    """Call the LLM to generate a natural summary. Use a high max_tokens so long analyses are not truncated."""
    prompt_messages = []
    llm = None
    try:
        llm = get_llm(temperature=0.5, max_tokens=8192)
        prompt_messages = [
            SystemMessage(content=_SYSTEM_PROMPT),
            HumanMessage(content=user_msg),
        ]
        response = llm.invoke(prompt_messages)
        trace_context = {"user_msg": user_msg[:500]}
        if state:
            trace_context.update(
                {
                    "workflow_id": state.get("workflow_id_requested") or (state.get("workflow_plan") or {}).get("workflow_id"),
                    "current_step_id": state.get("current_step_id"),
                }
            )
        return response.content, build_llm_trace_entry(
            node="responder",
            purpose="summary_reply",
            prompt_messages=prompt_messages,
            response=response,
            status="success",
            parsed_output={"reply_length": len(str(response.content or ""))},
            context=trace_context,
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )
    except Exception as e:
        logger.error("LLM summary generation failed: %s", e)
        trace_context = {"user_msg": user_msg[:500]}
        if state:
            trace_context.update(
                {
                    "workflow_id": state.get("workflow_id_requested") or (state.get("workflow_plan") or {}).get("workflow_id"),
                    "current_step_id": state.get("current_step_id"),
                }
            )
        return None, build_llm_trace_entry(
            node="responder",
            purpose="summary_reply",
            prompt_messages=prompt_messages,
            response=None,
            status="error",
            parsed_output=None,
            error=str(e),
            context=trace_context,
            model=str(getattr(llm, "model_name", "") or getattr(llm, "model", "") or ""),
        )


def _fallback_summary(
    goal: str,
    plan_status: str,
    stdout: str,
    artifacts: list,
) -> str:
    """Template-based fallback when LLM is unavailable. Lists all outputs and matches goal."""
    parts = ["Done. "]
    if artifacts:
        parts.append("**Outputs produced:**\n")
        for art in artifacts:
            name = art.get("filename", "")
            typ = art.get("type", "file")
            size = art.get("size_bytes", 0)
            preview = art.get("preview_data", "")
            line = f"- **{name}** ({typ}"
            if size:
                line += f", {size} bytes"
            line += ")"
            if preview and isinstance(preview, str):
                first_line = preview.split("\n")[0][:80]
                if first_line:
                    line += f" — e.g. {first_line}"
            line += "\n"
            parts.append(line)
        parts.append("")
    if stdout:
        parts.append("**Run output:** ")
        first_lines = [l.strip() for l in stdout.strip().split("\n")[:2] if l.strip()]
        if first_lines:
            parts.append(" ".join(first_lines)[:200] + "\n")
        else:
            parts.append("(see execution log for details).\n")
    parts.append(f"*Status: {plan_status}*")
    parts.append("If you want more detail on any output, say which one; or say **continue** for the next step.")
    return "\n".join(parts) if parts else f"Done. Completed. Goal: {goal}. Status: {plan_status}. Say **continue** or ask for more."


def _collect_step_attachments(
    artifact_index: List[Dict[str, Any]],
    step_id: str,
) -> List[Dict[str, Any]]:
    """Return a list of attachment dicts for artifacts from the current step."""
    attachments: List[Dict[str, Any]] = []
    for art in artifact_index:
        if art.get("step_id") != step_id:
            continue
        art_type = art.get("type", "file")
        att_type = "file"
        if art_type == "figure":
            att_type = "image"
        elif art_type == "table":
            att_type = "table"
        elif art_type in ("log", "report", "data"):
            att_type = "text"

        attachments.append({
            "type": att_type,
            "name": art.get("filename", ""),
            "path": art.get("path", ""),
            "preview": art.get("preview", ""),
            "artifactId": art.get("id", ""),
            "size": art.get("size_bytes", 0),
        })
    return attachments
