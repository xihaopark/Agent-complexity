from __future__ import annotations


class NewprojAgent:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def go(self, *args, **kwargs):
        raise NotImplementedError("NewprojAgent is not available in this runtime.")

