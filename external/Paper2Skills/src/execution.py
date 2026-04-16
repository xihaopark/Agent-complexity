"""Execution results from the agent (minimal; no sandbox/PDF)."""
from typing import List, Dict, Optional
import json


class ExecutionResults:
    """Minimal execution results: message history, code results, final response, token usage."""

    def __init__(
        self,
        message_history: List[Dict[str, str]],
        code_execution_results: List[Dict[str, str]],
        final_response: str,
        sandbox: Optional[object] = None,
        token_usage: Optional[Dict] = None,
    ):
        self.sandbox = sandbox
        self.message_history = message_history
        self.code_execution_results = code_execution_results
        self.final_response = final_response
        self.token_usage = token_usage

    def __str__(self) -> str:
        lines = []
        lines.append("=" * 80)
        lines.append("EXECUTION RESULTS")
        lines.append("=" * 80)
        lines.append(f"\nMessage History ({len(self.message_history)} messages):")
        lines.append("-" * 80)
        for i, msg in enumerate(self.message_history, 1):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            content_preview = content[:200] + "..." if len(content) > 200 else content
            lines.append(f"  [{i}] {role.upper()}:")
            lines.append(f"      {content_preview}")
            if i < len(self.message_history):
                lines.append("")
        lines.append("\n" + "-" * 80)
        lines.append(f"Code Execution Results ({len(self.code_execution_results)} executions):")
        lines.append("-" * 80)
        for i, result in enumerate(self.code_execution_results, 1):
            lines.append(f"  Execution #{i}:")
            for key, value in result.items():
                if isinstance(value, str):
                    value_preview = value[:150] + "..." if len(value) > 150 else value
                    lines.append(f"    {key}: {value_preview}")
                else:
                    lines.append(f"    {key}: {value}")
            if i < len(self.code_execution_results):
                lines.append("")
        lines.append("\n" + "-" * 80)
        lines.append("Final Response:")
        lines.append("-" * 80)
        for line in self.final_response.split("\n"):
            lines.append(f"  {line}")
        if self.token_usage:
            lines.append("\n" + "-" * 80)
            lines.append("Token Usage:")
            lines.append("-" * 80)
            totals = self.token_usage.get("totals", {})
            avgs = self.token_usage.get(
                "averages_per_doc", self.token_usage.get("averages_per_paper", {})
            )
            lines.append(f"  Model:            {self.token_usage.get('model', '?')}")
            lines.append(f"  Run duration:     {self.token_usage.get('run_duration_seconds', 0):.0f}s")
            lines.append(
                f"  Documents:        {self.token_usage.get('docs_completed', 0)} completed, "
                f"{self.token_usage.get('docs_skipped', 0)} skipped"
            )
            lines.append(f"  Total input:      {totals.get('input_tokens', 0):,}")
            lines.append(f"  Total output:     {totals.get('output_tokens', 0):,}")
            lines.append(f"  Total tokens:     {totals.get('total_tokens', 0):,}")
            lines.append(f"  Total LLM calls:  {totals.get('llm_calls', 0):,}")
            if avgs:
                lines.append(f"  Avg input/doc:    {avgs.get('input_tokens', 0):,}")
                lines.append(f"  Avg output/doc:   {avgs.get('output_tokens', 0):,}")
                lines.append(f"  Avg total/doc:    {avgs.get('total_tokens', 0):,}")
                lines.append(f"  Avg calls/doc:    {avgs.get('llm_calls', 0)}")
                lines.append(f"  Avg time/doc:     {avgs.get('duration_seconds', 0):.0f}s")
        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    def __repr__(self) -> str:
        return (
            f"ExecutionResults(messages={len(self.message_history)}, "
            f"executions={len(self.code_execution_results)}, "
            f"has_sandbox={self.sandbox is not None}, "
            f"has_token_usage={self.token_usage is not None})"
        )

    def to_json(self, output_path: Optional[str] = None) -> dict:
        """Convert the execution results to a JSON-serializable dict; optionally save to file."""
        data = {
            "message_history": self.message_history,
            "code_execution_results": self.code_execution_results,
            "final_response": self.final_response,
            "token_usage": self.token_usage,
        }
        if output_path is not None:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        return data
