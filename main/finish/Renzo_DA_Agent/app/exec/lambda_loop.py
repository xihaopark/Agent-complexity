from __future__ import annotations

from typing import Dict


class ProgrammerInspectorLoop:
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts

    def run(self, code: str, executor) -> Dict:
        attempts = 0
        last_result = None
        while attempts <= self.max_attempts:
            result = executor(code)
            last_result = result
            if result.get("status") == "success":
                break
            attempts += 1
        return {"attempts": attempts, "result": last_result}
