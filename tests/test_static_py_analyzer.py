from __future__ import annotations

from pathlib import Path

from analyzers.static_py.analyzer import analyze_python_repo


def test_analyze_python_repo_returns_core_metrics(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text(
        "\n".join(
            [
                "import os",
                "def run(x):",
                "    if x > 0:",
                "        try:",
                "            return os.getenv('A')",
                "        except Exception:",
                "            return 'fallback'",
                "    return 'done'",
            ]
        ),
        encoding="utf-8",
    )
    artifact_dir = tmp_path / "artifacts"
    metrics, artifacts = analyze_python_repo(repo, artifact_dir)
    codes = {m.metric_code for m in metrics}
    assert "A1" in codes
    assert "A8" in codes
    assert "F1" in codes
    assert len(artifacts) >= 1
