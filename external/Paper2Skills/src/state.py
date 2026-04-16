"""Agent state and code execution result types."""
from pydantic import BaseModel, Field
from typing import List, Annotated, Sequence

from langgraph.graph.message import add_messages, BaseMessage


class CodeExecutionResult(BaseModel):
    code: str
    console_output: str

    def __str__(self):
        return f"Code: {self.code}\nConsole Output: {self.console_output}"


class AgentState(BaseModel):
    """The state of the agent."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    code_execution_results: List[CodeExecutionResult] = []
