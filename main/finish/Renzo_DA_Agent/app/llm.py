"""
Lightweight LLM adapter for the agent system.

Uses OpenRouter as the API gateway, defaulting to Claude.
Supports switching models via the LLM_MODEL environment variable.

Usage:
    from renzo.app.llm import get_llm
    llm = get_llm()
    response = llm.invoke([HumanMessage(content="Hello")])
"""
from __future__ import annotations

import os
from functools import lru_cache

from langchain_openai import ChatOpenAI


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
_DEFAULT_MODEL = "deepseek/deepseek-r1"
_DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
_DEFAULT_TEMPERATURE = 0.2
_DEFAULT_MAX_TOKENS = 4096


def get_llm(
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> ChatOpenAI:
    """Return a ChatOpenAI instance configured for OpenRouter.

    Parameters
    ----------
    model : str, optional
        Model identifier (e.g. "anthropic/claude-sonnet-4-20250514").
        Falls back to ``LLM_MODEL`` env var, then to the built-in default.
    temperature : float, optional
        Sampling temperature. Defaults to 0.2 for deterministic planning.
    max_tokens : int, optional
        Maximum tokens in the response.

    Returns
    -------
    ChatOpenAI
        A LangChain chat model instance ready to use.
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY environment variable is not set. "
            "Please set it in your .env file or environment."
        )

    model = model or os.environ.get("LLM_MODEL") or os.environ.get("OPENROUTER_MODEL", _DEFAULT_MODEL)
    temperature = temperature if temperature is not None else _DEFAULT_TEMPERATURE
    max_tokens = max_tokens or int(os.environ.get("LLM_MAX_TOKENS", str(_DEFAULT_MAX_TOKENS)))

    timeout = int(os.environ.get("LLM_TIMEOUT", "60"))

    return ChatOpenAI(
        model=model,
        openai_api_key=api_key,
        openai_api_base=_DEFAULT_BASE_URL,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        max_retries=1,
        # OpenRouter-specific headers (optional but recommended)
        default_headers={
            "HTTP-Referer": "https://github.com/renzo",
            "X-Title": "Renzo Data Agent",
        },
    )
