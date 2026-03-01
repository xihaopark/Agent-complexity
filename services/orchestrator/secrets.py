from __future__ import annotations

import logging
import time
from uuid import uuid4

try:
    from redis import Redis  # type: ignore
except Exception:  # pragma: no cover
    Redis = None  # type: ignore

from common.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class SecretStore:
    def __init__(self) -> None:
        self._memory: dict[str, tuple[str, float]] = {}
        self.redis = Redis.from_url(settings.redis_url) if Redis is not None else None

    def put_token(self, token: str, ttl_seconds: int = 3600) -> str:
        ref = f"secret:{uuid4()}"
        if self.redis is not None:
            self.redis.set(name=ref, value=token, ex=ttl_seconds)
        else:
            self._memory[ref] = (token, time.time() + ttl_seconds)
        return ref

    def pop_token(self, ref: str | None) -> str | None:
        if not ref:
            return None
        if self.redis is not None:
            with self.redis.pipeline() as pipe:
                pipe.get(ref)
                pipe.delete(ref)
                token, _ = pipe.execute()
            if token is None:
                return None
            if isinstance(token, bytes):
                return token.decode("utf-8")
            return str(token)
        token, expire_at = self._memory.pop(ref, (None, 0))
        if token is None or time.time() > expire_at:
            return None
        return token


def get_secret_store() -> SecretStore:
    return SecretStore()
