"""Base runner interface for workflow execution."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class RunResult:
    """Result of a runner execution."""
    status: str  # success / error / timeout
    stdout: str = ""
    stderr: str = ""
    returncode: int = 0
    artifacts: List[str] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseRunner(ABC):
    """Abstract base class for workflow runners.
    
    Runners are tools that execute workflow steps and return results.
    The state machine (Planner/Executor) controls the flow; runners just execute.
    """

    @abstractmethod
    def run_step(
        self,
        workflow_dir: Path,
        work_dir: Path,
        targets: Optional[List[str]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> RunResult:
        """Execute a workflow step.
        
        Args:
            workflow_dir: Path to workflow definition (Snakefile, main.nf, etc.)
            work_dir: Working directory for execution (inputs, outputs, logs)
            targets: Specific targets/rules to execute (for Snakemake)
            params: Additional parameters
            timeout: Execution timeout in seconds
            
        Returns:
            RunResult with status, outputs, and artifacts
        """
        pass

    @abstractmethod
    def check_available(self) -> bool:
        """Check if this runner is available (engine installed)."""
        pass

    @abstractmethod
    def list_targets(self, workflow_dir: Path) -> List[str]:
        """List available targets/rules in a workflow."""
        pass

    def install_if_missing(self) -> bool:
        """Attempt to install the runner engine if missing.
        
        Returns True if installation succeeded or engine already available.
        Default implementation does nothing.
        """
        return self.check_available()
