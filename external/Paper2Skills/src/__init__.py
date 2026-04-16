"""Paper2Skills: minimal runnable Paper2SkillCreator (local workspace, no sandbox)."""

def __getattr__(name: str):
    if name == "Paper2SkillCreator":
        from src.agents.scientific_skills_creator import Paper2SkillCreator
        return Paper2SkillCreator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["Paper2SkillCreator"]
