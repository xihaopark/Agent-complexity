# Paper2Skills

Minimal runnable **Paper2SkillCreator** agent: explore training documents (papers, PDFs, folders) and build a **git-managed Python skill library** in a local workspace. No Docker/sandbox — all tools run on the local filesystem. Suitable for sharing with external users without proprietary BioDSA internals.

## Setup

```bash
cd Paper2Skills
pipenv install
```

Requires Python 3.12. Dependencies are in `Pipfile`.

## Environment

Create a `.env` file (or export variables) with your LLM API credentials:

- **Azure OpenAI**: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`
- For OpenAI/Anthropic/Google, adjust `run_skill_creator.py` to use the appropriate `api_type` and env vars.

## Usage

1. **Workspace**: A **git** repository that will hold the skill package (e.g. clone or init a repo).
2. **Training data**: A directory whose top-level items (files or folders) are each treated as one document to process.

Edit `run_skill_creator.py` to set:

- `workspace_dir` — path to the git repo (skill library root).
- `skill_name` — name of the skill package inside the repo (e.g. `clinical_trials`, `rwd_skills`).
- `train_data_dir` — path to the directory containing papers/PDFs/folders to process.

Then run:

```bash
python run_skill_creator.py
```

The agent will create a timestamped branch (e.g. `skill/run-YYYYMMDD-HHMMSS`), process each document in `train_data_dir`, and write/update Python modules, tests, and SKILL.md files under `<workspace_dir>/<skill_name>/`. It does not merge; you merge the branch when ready.

Example outputs:

```bash
🤖 AI Assistant
====================================================================================================

📞 Tool Calls (1):
  [1] bash_in_workspace
      command: ls -la

====================================================================================================
🔧 Tool Response (bash_in_workspace)
====================================================================================================
$ ls -la

stdout:
total 528
drwxrwxr-x.  8 ec2-user ec2-user  16384 Feb 12 14:34 .
drwxrwxr-x. 11 ec2-user ec2-user  16384 Mar  7 02:31 ..
drwxrwxr-x.  7 ec2-user ec2-user    186 Mar  7 02:51 .git
-rw-rw-r--.  1 ec2-user ec2-user   4739 Feb 12 13:57 .gitignore
drwxrwxr-x.  3 ec2-user ec2-user     70 Feb 12 12:48 .pytest_cache
-rw-rw-r--.  1 ec2-user ec2-user   1237 Feb 12 14:58 .todos.json
drwxrwxr-x.  2 ec2-user ec2-user     86 Feb 12 14:58 .token_reports
-rw-rw-r--.  1 ec2-user ec2-user   1063 Feb 12 12:06 LICENSE
-rw-rw-r--.  1 ec2-user ec2-user    923 Feb 12 14:03 Pipfile
-rw-r--r--.  1 ec2-user ec2-user 480489 Feb 12 13:30 Pipfile.lock
-rw-rw-r--.  1 ec2-user ec2-user     25 Feb 12 12:06 README.md
drwxrwxr-x.  6 ec2-user ec2-user    178 Feb 12 14:50 clinical_trials
drwxrwxr-x.  5 ec2-user ec2-user     91 Feb 12 14:34 data
drwxrwxr-x.  5 ec2-user ec2-user    159 Feb 12 14:05 observational_studies

returncode: 0

====================================================================================================
🤖 AI Assistant
====================================================================================================

📞 Tool Calls (1):
  [1] glob_files
      pattern: **/*.pdf

====================================================================================================
🔧 Tool Response (glob_files)
====================================================================================================
Found 2 file(s) matching "**/*.pdf" (newest first):
data/clinical-trials-train/PMC11488644.pdf
data/clinical-trials-train/PM38912654.pdf

====================================================================================================
🤖 AI Assistant
====================================================================================================

📞 Tool Calls (1):
  [1] read_pdf
      pdf_path: data/clinical-trials-train/PMC11488644.pdf
      page_range: 1-3

====================================================================================================
🔧 Tool Response (read_pdf)
====================================================================================================
PDF loaded as images: PMC11488644.pdf (3/17 pages).
[3 image(s) attached]

====================================================================================================
🤖 AI Assistant
====================================================================================================

📞 Tool Calls (1):
  [1] read_pdf
      pdf_path: data/clinical-trials-train/PMC11488644.pdf
      search_query: Methods|Statistical|analysis|endpoint|outcome

====================================================================================================
🔧 Tool Response (read_pdf)
====================================================================================================
PDF loaded as images: PMC11488644.pdf (17/17 pages).
[17 image(s) attached]

====================================================================================================
🤖 AI Assistant
====================================================================================================

📞 Tool Calls (1):
  [1] read_pdf
      pdf_path: data/clinical-trials-train/PMC11488644.pdf
      page_range: 6-10

====================================================================================================
🔧 Tool Response (read_pdf)
====================================================================================================
PDF loaded as images: PMC11488644.pdf (5/17 pages).
[5 image(s) attached]

====================================================================================================
🤖 AI Assistant
====================================================================================================

📞 Tool Calls (1):
  [1] read_pdf
      pdf_path: data/clinical-trials-train/PM38912654.pdf
      page_range: 1-3

====================================================================================================
🔧 Tool Response (read_pdf)
====================================================================================================
PDF loaded as images: PM38912654.pdf (3/22 pages).
[3 image(s) attached]

```

## What this repo includes

- **Paper2SkillCreator** agent (LangGraph + tools).
- **Local-only tool wrappers**: file write/edit, bash in workspace, glob/grep, read_image, read_pdf, todo_write, processed-state, run_tests.
- **Slim base agent**: no sandbox, no Docker; workdir is a local path only.
- **Minimal execution results**: message history, final response, token usage (no PDF report, no artifact download).

## What this repo does not include

- Docker/sandbox or any execution environment.
- BioDSA proprietary tools (risk calculators, clinical trials APIs, etc.) or other agents.

## License

See [LICENSE](LICENSE).
