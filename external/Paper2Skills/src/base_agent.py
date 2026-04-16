"""
Slim BaseAgent: no sandbox, local workdir only.
Content-filter helpers, run_with_retry, LLM factory, message formatting, compaction.
"""
import os
import logging
from typing import Dict, Any, Callable, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.tools import BaseTool
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage, HumanMessage
from langchain_core.messages.utils import count_tokens_approximately
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import BaseMessage
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

from src.state import CodeExecutionResult
from src.utils.render_utils import render_message_colored
from src.llm_config import (
    SupportedApiType,
    SupportedModelName,
    ALL_SUPPORTED_MODELS,
)


# ------------------------------------------------------------------ #
# Content-filter helpers
# ------------------------------------------------------------------ #


class ContentFilterError(Exception):
    """Raised when the LLM provider rejects a prompt due to content policy."""

    def __init__(self, original_error: Exception, filter_result: dict = None):
        self.original_error = original_error
        self.filter_result = filter_result or {}
        super().__init__(str(original_error))


def _is_content_filter_error(exc: Exception) -> bool:
    """Return True if *exc* is an Azure / OpenAI content-filter rejection."""
    msg = str(exc).lower()
    return (
        "content_filter" in msg
        or "content management policy" in msg
        or "responsibleaipolicyviolation" in msg
    )


def _strip_images_from_messages(messages: List[BaseMessage]) -> List[BaseMessage]:
    """Return a copy of *messages* with all image content blocks removed."""
    cleaned: List[BaseMessage] = []
    for msg in messages:
        content = msg.content
        if isinstance(content, list):
            new_blocks: list = []
            had_images = False
            for block in content:
                if isinstance(block, dict):
                    btype = block.get("type", "")
                    if btype in ("image", "image_url"):
                        had_images = True
                        continue
                    new_blocks.append(block)
                else:
                    new_blocks.append(block)
            if had_images:
                new_blocks.append(
                    {"type": "text", "text": "[images removed for content-filter compliance]"}
                )
            new_msg = msg.model_copy(update={"content": new_blocks})
            cleaned.append(new_msg)
        else:
            cleaned.append(msg)
    return cleaned


def _should_not_retry(exc: Exception) -> bool:
    return _is_content_filter_error(exc)


def run_with_retry(
    func: Callable,
    max_retries: int = 5,
    min_wait: float = 1.0,
    max_wait: float = 30.0,
    timeout: Optional[float] = None,
    arg=None,
    **kwargs,
):
    """Execute a function with exponential backoff; content-filter errors are not retried."""
    @retry(
        stop=stop_after_attempt(max_retries),
        wait=wait_random_exponential(multiplier=min_wait, max=max_wait),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def wrapped_func():
        try:
            if timeout is not None:
                executor = ThreadPoolExecutor(max_workers=1)
                try:
                    if arg is not None:
                        future = executor.submit(func, arg)
                    else:
                        future = executor.submit(func, **kwargs)
                    try:
                        return future.result(timeout=timeout)
                    except FuturesTimeoutError:
                        logging.warning(
                            "Timeout exceeded: %s did not complete within %s seconds",
                            getattr(func, "__name__", "func"),
                            timeout,
                        )
                        future.cancel()
                        raise TimeoutError(
                            f"{getattr(func, '__name__', 'func')} exceeded timeout of {timeout} seconds"
                        )
                finally:
                    executor.shutdown(wait=False)
            else:
                if arg is not None:
                    return func(arg)
                return func(**kwargs)
        except Exception as e:
            if _should_not_retry(e):
                logging.warning(
                    "Content-filter error detected — raising immediately (no retry)."
                )
                raise
            logging.warning("Retry triggered: %s failed with error: %s", getattr(func, "__name__", "func"), e)
            raise

    return wrapped_func()


class BaseAgent:
    """Slim base agent: no sandbox, local workdir only."""

    system_prompt: Optional[str] = None
    sandbox: None = None
    workdir: str = None  # type: ignore[assignment]

    def __init__(
        self,
        api_type: SupportedApiType,
        api_key: str,
        model_name: SupportedModelName = None,  # type: ignore[assignment]
        endpoint: str = None,  # type: ignore[assignment]
        max_completion_tokens: int = 5000,
        container_id: str = None,  # unused; kept for API compatibility
        model_kwargs: Dict[str, Any] = None,
        llm_timeout: Optional[float] = None,
        **kwargs,
    ):
        self.sandbox = None
        self.workdir = os.path.join(os.getcwd(), "workdir")
        os.makedirs(self.workdir, exist_ok=True)

        self.endpoint = endpoint
        self.api_key = api_key
        self.model_name = model_name
        if model_name is not None and model_name not in ALL_SUPPORTED_MODELS:
            logging.warning(
                "model_name %r not in llm_config.ALL_SUPPORTED_MODELS; "
                "add it to src.llm_config if this is a supported model.",
                model_name,
            )
        self.api_type = api_type
        self.max_completion_tokens = max_completion_tokens
        self.model_kwargs = model_kwargs or {}
        self.llm_timeout = llm_timeout

        self.llm = self._get_model(
            api=self.api_type,
            model_name=self.model_name,
            api_key=self.api_key,
            endpoint=self.endpoint,
            **kwargs,
        )

    def _get_model(
        self,
        api: str,
        api_key: str,
        model_name: str,
        endpoint: str = None,
        **kwargs,
    ) -> BaseLanguageModel:
        if model_name not in ["o3-mini", "o3-preview"]:
            kwargs.pop("max_completion_tokens", None)

        if api == "anthropic":
            return ChatAnthropic(
                model=model_name,
                api_key=api_key,
                max_retries=0,
                **kwargs,
            )
        if api == "openai":
            return ChatOpenAI(
                model=model_name,
                api_key=api_key,
                max_retries=0,
                **kwargs,
            )
        if api == "google":
            return ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                max_retries=0,
                **kwargs,
            )
        if api == "azure":
            kwargs = {k: v for k, v in kwargs.items() if k != "reasoning_effort"}
            return AzureChatOpenAI(
                azure_endpoint=endpoint,
                azure_deployment=model_name,
                api_key=api_key,
                api_version="2024-12-01-preview",
                max_retries=0,
                **kwargs,
            )
        raise ValueError(f"Invalid API: {api}")

    def _format_messages(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        outputs = []
        for message in messages:
            msg_content = message.content
            if isinstance(msg_content, list):
                content_parts = []
                for block in msg_content:
                    if isinstance(block, dict):
                        if "text" in block:
                            content_parts.append(block["text"])
                        elif block.get("type") == "text" and "text" in block:
                            content_parts.append(block["text"])
                        else:
                            content_parts.append(str(block))
                    elif isinstance(block, str):
                        content_parts.append(block)
                    else:
                        content_parts.append(str(block))
                msg_content = "".join(content_parts)
            elif not isinstance(msg_content, str):
                msg_content = str(msg_content)

            if hasattr(message, "tool_calls") and message.tool_calls:
                msg_tool_calls = message.tool_calls if isinstance(message.tool_calls, list) else [message.tool_calls]
                for tc in msg_tool_calls:
                    msg_content += f"\nTool call: {tc['name']}\nTool call input: {tc.get('args', {})}"
            outputs.append({"role": message.type, "content": msg_content})
        return outputs

    def _format_code_execution_results(
        self, code_execution_results: List[CodeExecutionResult]
    ) -> List[Dict[str, str]]:
        return [res.model_dump() for res in code_execution_results]

    def _set_model_kwargs(self, model_name: str) -> Dict[str, Any]:
        model_kwargs = {}
        if "claude" in model_name.lower():
            model_kwargs["thinking"] = {"type": "enabled", "budget_tokens": 5000}
            model_kwargs["max_tokens"] = 10000
            model_kwargs.pop("reasoning_effort", None)
        if "gpt" in model_name.lower():
            model_kwargs["reasoning_effort"] = "medium"
            model_kwargs.pop("thinking", None)
            model_kwargs["max_completion_tokens"] = 5000
        return model_kwargs

    @staticmethod
    def _print_message(message: BaseMessage, show_tool_calls: bool = True) -> None:
        print(render_message_colored(message, show_tool_calls=show_tool_calls))

    def _print_stream_chunk(self, chunk: Dict[str, Any], show_tool_calls: bool = True) -> None:
        messages = chunk.get("messages")
        if not messages:
            return
        self._print_message(messages[-1], show_tool_calls=show_tool_calls)

    @staticmethod
    def _build_tool_message(tool_output: Any, name: str, tool_call_id: str) -> ToolMessage:
        from src.tool_wrappers.multimodal_tools import MultimodalToolResult

        if isinstance(tool_output, MultimodalToolResult):
            content = tool_output.to_langchain_content()
            return ToolMessage(content=content, name=name, tool_call_id=tool_call_id)
        return ToolMessage(content=str(tool_output), name=name, tool_call_id=tool_call_id)

    @staticmethod
    def _content_to_text(content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: List[str] = []
            for block in content:
                if isinstance(block, dict):
                    btype = block.get("type", "")
                    if btype == "text":
                        parts.append(block.get("text", ""))
                    elif btype in ("image", "image_url"):
                        parts.append("[image]")
                    elif btype in ("file", "audio", "video"):
                        parts.append(f"[{btype}]")
                elif isinstance(block, str):
                    parts.append(block)
            return "\n".join(parts)
        return str(content)

    def _compact_messages(
        self,
        messages: List[BaseMessage],
        token_threshold: int = 80000,
        compact_model_name: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> List[BaseMessage]:
        token_count = count_tokens_approximately(messages)
        if token_count <= token_threshold:
            return messages

        compact_model = compact_model_name or "gpt-5-mini"
        call_timeout = timeout if timeout is not None else self.llm_timeout
        logging.info(
            "compact_messages: ~%d tokens (threshold %d); summarising with %s.",
            token_count, token_threshold, compact_model,
        )

        system_msg = messages[0] if messages and isinstance(messages[0], SystemMessage) else None
        first_human_idx = next(
            (i for i, m in enumerate(messages) if isinstance(m, HumanMessage)),
            None,
        )
        if system_msg is None or first_human_idx is None:
            return messages
        user_msg = messages[first_human_idx]
        middle = messages[first_human_idx + 1:]
        if not middle:
            return messages

        text_parts = []
        for m in middle:
            role = getattr(m, "type", type(m).__name__)
            content = self._content_to_text(getattr(m, "content", "") or "")
            if isinstance(m, AIMessage) and getattr(m, "tool_calls", None):
                tc = m.tool_calls[0]
                text_parts.append(
                    f"[{role}] Called tool '{tc.get('name', '?')}' with args: {tc.get('args', {})}\n{content}"
                )
            elif isinstance(m, ToolMessage):
                name = getattr(m, "name", "?")
                text_parts.append(f"[{role} ({name})]\n{content}")
            else:
                text_parts.append(f"[{role}]\n{content}")
        background_text = "\n---\n".join(text_parts)

        compact_llm = self._get_model(
            api=self.api_type,
            model_name=compact_model,
            api_key=self.api_key,
            endpoint=self.endpoint,
        )
        summary_prompt = [
            SystemMessage(content=(
                "You are a concise summarizer. Summarize the following agent "
                "conversation history into a compact background briefing. "
                "Focus on: what actions were taken (tool calls and results), "
                "key findings, what was created/updated, and any errors. "
                "Keep it concise (under 1000 words). Do NOT include raw file "
                "contents; just note what was read and the key takeaways."
            )),
            HumanMessage(content=f"Conversation history to summarize:\n\n{background_text}"),
        ]
        try:
            summary_response = run_with_retry(
                compact_llm.invoke, arg=summary_prompt, timeout=call_timeout
            )
            summary_text = summary_response.content or ""
        except Exception as e:
            logging.warning("compact_messages failed (%s); returning original.", e)
            return messages

        compacted = [
            system_msg,
            SystemMessage(content=(
                "# Background (compacted from earlier conversation)\n\n" + summary_text
            )),
            user_msg,
        ]
        new_count = count_tokens_approximately(compacted)
        logging.info(
            "compact_messages: ~%d → ~%d tokens (summary %d chars).",
            token_count, new_count, len(summary_text),
        )
        return compacted
