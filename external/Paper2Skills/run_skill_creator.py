"""Run Paper2SkillCreator: explore training data and build a git-managed skill library."""
import os
from dotenv import load_dotenv

load_dotenv()

from src.agents.scientific_skills_creator import Paper2SkillCreator

agent = Paper2SkillCreator(
    model_name="gpt-5.2",
    api_type="azure",
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    recursion_limit=100,
    compact_token_threshold=100000,
    compact_model_name="gpt-5-mini",
)

agent.register_workspace(
    workspace_dir="/home/ec2-user/github/agentic-scientific-skills", # change this to your own github repository
)

agent.go(
    "Explore the materials and create skills.",
    skill_name="clinical_trials",
    train_data_dir="./example_data/clinical-trials-papers-train",
)
