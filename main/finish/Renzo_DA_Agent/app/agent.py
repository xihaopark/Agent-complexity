from __future__ import annotations

import logging
import os
import queue
import threading
from pathlib import Path
from typing import Generator, List, Optional

# Load .env before anything that needs env vars (LLM keys, etc.)
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass  # dotenv not installed — rely on env vars being set externally

from langchain_core.messages import HumanMessage

from renzo.app.graph import build_graph
from renzo.app.state import default_state
from renzo.app.knowhow import KnowHowLoader, find_skill_files, find_workflow_skill_specs

logger = logging.getLogger(__name__)

# Sentinel to signal end of streaming
_STREAM_DONE = object()

# Safety limit to prevent infinite loops in the LangGraph.
# A single step cycle is ~14 node transitions. With 8 steps + retries, 200 is generous.
# Override with GRAPH_RECURSION_LIMIT env (e.g. 400 for longer workflows).
def _graph_config() -> dict:
    limit = int(os.environ.get("GRAPH_RECURSION_LIMIT", "200"))
    return {"recursion_limit": limit}


class RenzoAgent:
    """Main agent entry point.

    Features:
      - Multi-language code execution (Python + R)
      - Human-in-the-Loop (HITL) support
      - Know-how / domain knowledge injection
      - LangGraph state machine with planning, coding, execution, QC
      - Real-time streaming of intermediate node states

    Usage:
        agent = RenzoAgent()

        # Optionally load domain knowledge
        agent.add_know_how("path/to/clinical-pipeline.md")

        # Stream intermediate updates
        for update in agent.stream("Create ADSL from SDTM DM dataset"):
            print(update["current_node"])  # See each node as it runs

        # Or run synchronously
        result = agent.go("Create ADSL from SDTM DM dataset")
    """

    def __init__(self, auto_load_skills: bool = True):
        self.app = build_graph()
        self.state = default_state()
        self.know_how_loader = KnowHowLoader()

        if auto_load_skills:
            self._auto_load_skills()

    def _know_how_max_chars(self) -> int:
        return int(os.environ.get("KNOW_HOW_MAX_CHARS", "20000"))

    def _refresh_know_how_state(self) -> None:
        if self.know_how_loader.documents:
            self.state["know_how_context"] = self.know_how_loader.get_context(
                max_chars=self._know_how_max_chars()
            )
            self.state["know_how_documents"] = self.know_how_loader.list_documents()
        else:
            self.state["know_how_context"] = ""
            self.state["know_how_documents"] = []

    def _auto_load_skills(self) -> None:
        """Automatically discover and load skill files from project skill directories."""
        try:
            skill_files = find_skill_files()
            for skill_path in skill_files:
                self.know_how_loader.add_from_file(skill_path)

            if self.know_how_loader.documents:
                self._refresh_know_how_state()
                logger.info(
                    "Auto-loaded %d skill document(s): %s",
                    len(self.know_how_loader.documents),
                    [d.name for d in self.know_how_loader.documents],
                )
        except Exception as e:
            logger.warning("Failed to auto-load skills: %s", e)

    def add_know_how(self, source: str, name: Optional[str] = None,
                     description: Optional[str] = None) -> str:
        """Add a know-how document from a file path or string content."""
        if os.path.isfile(source):
            doc_id = self.know_how_loader.add_from_file(source, name, description)
        else:
            doc_id = self.know_how_loader.add_from_string(source, name, description)

        self._refresh_know_how_state()
        return doc_id

    def get_know_how_summary(self) -> List[dict]:
        """List all loaded know-how documents."""
        return self.know_how_loader.list_documents()

    def load_workflow_skills(
        self,
        workflow_id: str,
        *,
        base_dir: Optional[str] = None,
        clear_existing: bool = False,
    ) -> List[dict]:
        """Load only the standardized skills that belong to a workflow."""
        if clear_existing:
            self.know_how_loader.clear()

        specs = find_workflow_skill_specs(workflow_id, base_dir=base_dir)
        for spec in specs:
            self.know_how_loader.add_from_file(spec.source_path)

        self._refresh_know_how_state()
        return [spec.__dict__.copy() for spec in specs]

    def load_workflow_know_how(self, workflow_id: str) -> None:
        """Load know-how from a workflow's manifest if available.

        Called automatically when an experiment linked to a workflow starts.
        Idempotent: skips if already loaded for this workflow.
        """
        # Avoid re-loading
        loaded_ids = {d.id for d in self.know_how_loader.documents}
        tag_prefix = f"workflow_{workflow_id}_"
        if any(doc_id.startswith(tag_prefix) for doc_id in loaded_ids):
            return
        try:
            from renzo.app.wf_manager import get_workflow_know_how_documents
            docs = get_workflow_know_how_documents(workflow_id)
            for index, doc in enumerate(docs, start=1):
                tag = f"{tag_prefix}{index:02d}_{doc['id']}"
                self.know_how_loader.add_from_string(
                    doc["content"],
                    name=f"{workflow_id}: {doc['name']}",
                    description=f"Workflow know-how from {Path(doc['path']).name}",
                )
                if self.know_how_loader.documents:
                    self.know_how_loader.documents[-1].id = tag
                    self.know_how_loader._doc_index[tag] = self.know_how_loader.documents[-1]
            if docs:
                self._refresh_know_how_state()
                logger.info("Loaded %d workflow know-how document(s) for %s", len(docs), workflow_id)
        except Exception as e:
            logger.warning("Failed to load workflow know-how for %s: %s", workflow_id, e)

    def _prepare_run(self, prompt: str) -> dict:
        """Prepare state and inputs for a run.

        Preserves existing plan/artifacts across turns so the planner
        can resume, but resets per-turn routing flags.

        IMPORTANT: The returned dict is passed as `inputs` to the LangGraph.
        Any state field that needs to be visible to graph nodes must be
        included here — setting self.state alone does NOT propagate to
        the graph's internal state channels.

        We carry forward plan_steps, execution_logs, artifact_index, etc.
        so that the planner can detect "continue" and resume existing plans
        instead of creating a new one every turn.
        """
        self.state["goal"] = prompt
        self.state["terminate"] = False      # allow the graph to run
        self.state["next_node"] = "planner"  # default entry
        self.state["code_scratchpad"] = ""   # clear stale code
        self.state["validation_result"] = {} # clear stale validation
        self.state["retry_count"] = 0
        know_how_context = ""
        if self.know_how_loader.documents:
            know_how_context = self.know_how_loader.get_context(
                max_chars=self._know_how_max_chars()
            )
            self.state["know_how_context"] = know_how_context

        # Build the inputs dict.  Every state channel the graph needs
        # must be represented here; otherwise LangGraph starts with
        # the channel's default value (empty list, empty string, etc.).
        inputs = {
            "messages": [HumanMessage(content=prompt)],
            "goal": prompt,
            "know_how_context": know_how_context,
        }

        # Carry forward persistent state from previous turns so the
        # planner can detect "continue" and resume instead of replanning.
        _carry_forward_keys = [
            "plan_steps", "plan_version", "plan_status", "current_step_id",
            "execution_logs", "artifact_index", "data_profile",
            "code_language", "installed_packages",
            "workflow_plan", "workflow_status", "workflow_id_requested",
            "workflow_run_context", "execution_workdir", "artifact_policy",
            "qc_results", "experiment_id", "session_id",
            "dataset_context",
            "data_catalog", "data_lineage",
            "error_book",
        ]
        for key in _carry_forward_keys:
            val = self.state.get(key)
            if val is not None and val != "" and val != [] and val != {}:
                inputs[key] = val

        return inputs

    def stream(self, prompt: str) -> Generator[dict, None, None]:
        """Stream intermediate state updates from the agent graph.

        Yields a snapshot of the state dict after each node executes.
        The final yield is the complete state.
        """
        inputs = self._prepare_run(prompt)

        for output in self.app.stream(inputs, config=_graph_config(), stream_mode="values"):
            self.state.update(output)
            yield dict(self.state)

            if self.state.get("hitl_pending"):
                break

    def stream_to_queue(
        self,
        prompt: str,
        q: queue.Queue,
        cancel_event: Optional["threading.Event"] = None,
    ) -> None:
        """Run the agent graph and push snapshots to a thread-safe queue.

        Used by the async WebSocket handler: the graph runs in a thread,
        each node's output is pushed to the queue, and the async handler
        reads from the queue to send WebSocket updates in real-time.

        If cancel_event is set (e.g. user clicked Interrupt), the loop
        exits after the current node and puts _STREAM_DONE.
        """
        try:
            inputs = self._prepare_run(prompt)
            for output in self.app.stream(inputs, config=_graph_config(), stream_mode="values"):
                if cancel_event and cancel_event.is_set():
                    self.state["_stream_error"] = "Stopped by user (interrupt)."
                    q.put(dict(self.state))
                    break
                self.state.update(output)
                q.put(dict(self.state))
                if self.state.get("hitl_pending"):
                    break
        except Exception as e:
            logger.error("Agent stream error: %s", e, exc_info=True)
            self.state["_stream_error"] = str(e)
            q.put(dict(self.state))
        finally:
            q.put(_STREAM_DONE)

    def resume_after_hitl_to_queue(self, hitl_response: str, q: queue.Queue) -> None:
        """Resume the agent graph after receiving a HITL response.

        Instead of creating a fresh run with a new goal, this preserves the
        existing state (plan_steps, goal, etc.) and just injects the HITL
        response, then continues the graph from the router node.
        """
        try:
            # Inject HITL response into existing state without resetting goal
            self.state["hitl_response"] = hitl_response
            self.state["hitl_pending"] = False
            self.state["next_node"] = "planner"  # Route back to planner

            # Build inputs: keep existing state and add the HITL response.
            # Must carry forward plan_steps etc. — same as _prepare_run().
            inputs: dict = {
                "messages": [HumanMessage(content=f"[User clarification] {hitl_response}")],
                "hitl_response": hitl_response,
                "hitl_pending": False,
            }

            # Carry forward persistent state so the planner sees the
            # existing plan, execution logs, artifacts, etc.
            _carry_forward_keys = [
                "goal", "know_how_context",
                "plan_steps", "plan_version", "plan_status", "current_step_id",
                "execution_logs", "artifact_index", "data_profile",
                "code_language", "installed_packages",
                "workflow_plan", "workflow_status", "workflow_id_requested",
                "workflow_run_context", "execution_workdir", "artifact_policy",
                "qc_results", "experiment_id", "session_id",
                "dataset_context",
                "data_catalog", "data_lineage",
                "error_book",
            ]
            for key in _carry_forward_keys:
                val = self.state.get(key)
                if val is not None and val != "" and val != [] and val != {}:
                    inputs[key] = val

            for output in self.app.stream(inputs, config=_graph_config(), stream_mode="values"):
                self.state.update(output)
                q.put(dict(self.state))
                if self.state.get("hitl_pending"):
                    break
        except Exception as e:
            logger.error("Agent HITL resume error: %s", e, exc_info=True)
            self.state["_stream_error"] = str(e)
            q.put(dict(self.state))
        finally:
            q.put(_STREAM_DONE)

    def go(self, prompt: str) -> dict:
        """Run the agent synchronously (blocks until complete).

        For real-time updates, prefer ``stream()`` or ``stream_to_queue()``.
        """
        inputs = self._prepare_run(prompt)
        for output in self.app.stream(inputs, config=_graph_config(), stream_mode="values"):
            self.state.update(output)
            if self.state.get("hitl_pending"):
                break
        return self.state
