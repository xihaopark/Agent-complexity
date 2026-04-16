"""
Central config for supported LLM API types and model names.
Support: OpenAI, Anthropic, Google, Azure (OpenAI-compatible).
"""
from typing import Literal

SUPPORTED_API_TYPES = ("openai", "anthropic", "google", "azure")
SupportedApiType = Literal["openai", "anthropic", "google", "azure"]

OPENAI_MODELS = (
    "gpt-5.2", "gpt-5.2-codex", "gpt-5", "gpt-5-mini",
    "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-4.5-preview",
    "gpt-4o", "gpt-4o-mini", "gpt-4o-2024-11-20",
    "gpt-4-turbo", "gpt-4-turbo-preview", "gpt-4", "gpt-4-32k",
    "gpt-3.5-turbo", "gpt-3.5-turbo-16k",
    "o1", "o1-mini", "o1-preview", "o3", "o3-mini", "o3-preview", "o4-mini",
)

ANTHROPIC_MODELS = (
    "claude-opus-4-6", "claude-opus-4-6-20260205",
    "claude-sonnet-4-5", "claude-sonnet-4-5-20250929",
    "claude-haiku-4-5", "claude-haiku-4-5-20251001",
    "claude-sonnet-4-20250514",
    "claude-3-5-sonnet-20241022", "claude-3-5-sonnet",
    "claude-3-5-haiku-20241022", "claude-3-5-haiku",
    "claude-3-opus-20240229", "claude-3-opus",
    "claude-3-sonnet-20240229", "claude-3-sonnet",
    "claude-3-haiku-20240307", "claude-3-haiku",
)

GOOGLE_MODELS = (
    "gemini-3-pro-preview", "gemini-3-flash-preview", "gemini-3-pro-image-preview",
    "gemini-2.5-pro", "gemini-2.5-flash",
    "gemini-2.0-flash", "gemini-2.0-flash-lite",
    "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-flash-8b",
    "gemini-1.0-pro", "gemini-pro",
)

AZURE_MODELS = (
    "gpt-5.2", "gpt-5", "gpt-5-mini",
    "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-4.5-preview",
    "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-35-turbo",
    "o1", "o1-mini", "o3", "o3-mini", "o3-preview", "o4-mini",
)

ALL_SUPPORTED_MODELS = frozenset(
    OPENAI_MODELS + ANTHROPIC_MODELS + GOOGLE_MODELS + AZURE_MODELS
)

SupportedModelName = Literal[
    "gpt-5.2", "gpt-5.2-codex", "gpt-5", "gpt-5-mini",
    "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-4.5-preview",
    "gpt-4o", "gpt-4o-mini", "gpt-4o-2024-11-20",
    "gpt-4-turbo", "gpt-4-turbo-preview", "gpt-4", "gpt-4-32k",
    "gpt-3.5-turbo", "gpt-3.5-turbo-16k",
    "o1", "o1-mini", "o1-preview", "o3", "o3-mini", "o3-preview", "o4-mini",
    "claude-opus-4-6", "claude-opus-4-6-20260205",
    "claude-sonnet-4-5", "claude-sonnet-4-5-20250929",
    "claude-haiku-4-5", "claude-haiku-4-5-20251001",
    "claude-sonnet-4-20250514",
    "claude-3-5-sonnet-20241022", "claude-3-5-sonnet",
    "claude-3-5-haiku-20241022", "claude-3-5-haiku",
    "claude-3-opus-20240229", "claude-3-opus",
    "claude-3-sonnet-20240229", "claude-3-sonnet",
    "claude-3-haiku-20240307", "claude-3-haiku",
    "gemini-3-pro-preview", "gemini-3-flash-preview", "gemini-3-pro-image-preview",
    "gemini-2.5-pro", "gemini-2.5-flash",
    "gemini-2.0-flash", "gemini-2.0-flash-lite",
    "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-flash-8b",
    "gemini-1.0-pro", "gemini-pro",
    "gpt-35-turbo",
]
