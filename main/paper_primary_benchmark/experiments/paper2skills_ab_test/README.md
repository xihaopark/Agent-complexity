# Paper2Skills A/B test

Comparison between two paper-to-skill conversion strategies, so the
coordinator (Phase D of `COORDINATION_PLAN.md`) can pick one for the
`with-skill` arm of the ldp R-task benchmark.

## Two methods under test

| Method | Entry point | Input | LLM involved? |
|---|---|---|---|
| 1. vision-adapter (this dir) | `vision_adapter.py` | PDF → rendered PNG pages | OpenRouter `openai/gpt-4o` (vision) |
| 2. template | `main/paper_primary_benchmark/literature/tools/paper_to_skill.py` | PDF → `fitz` text (first ~8 pages) | none |

### Why not the full `external/Paper2Skills`

The original tool (`external/Paper2Skills/run_skill_creator.py`) is a
LangGraph + Azure-OpenAI + git-managed agent that writes Python modules
and pytest tests on a dedicated branch. Adapting it to run end-to-end in
this workspace within the ≤30-minute budget would require:

- Installing LangGraph + the whole `src.tool_wrappers.*` stack
  (`pipenv install` from its `Pipfile`, Python 3.12).
- Re-pointing `BaseAgent` at OpenRouter instead of Azure (custom
  `api_type` + reworking `_get_model`).
- Registering an external git repository as the skill library workspace.
- Running the vision/image path of `read_pdf` which ships bound to the
  agent's image transport.

Per the coordination plan we do **not** spend >30 minutes on this. We
instead wrote `vision_adapter.py` — a single-file OpenRouter-compatible
re-implementation that captures the essential behaviour the full tool
would contribute to comparing against Method 2: render PDF pages as
images and have a vision LLM distil them into structured sections.

What the full `external/Paper2Skills` adds over this adapter (read from
its `agent.py`/`prompt.py`/`tools.py`):

- Multi-step agent loop (LangGraph) with `todo_write`, `grep_files`,
  `glob_files`, `bash_in_workspace`, `run_tests`.
- Writes runnable **Python modules** (≤80 LOC each) + pytest tests +
  `docs/<method>.md` + topic-level `SKILL.md` index.
- Git branching per run, per-doc `mark_docs_processed` state.
- Token-accounting + compaction when conversations blow past
  `compact_token_threshold`.
- Content-filter self-heal (strips images on retry).

Those features matter for *building a reusable Python skill library*.
For our use case — a single SKILL.md snippet fed into an R-analysis
agent's system prompt — they add overhead without changing the
SKILL.md content quality compared to the adapter's single-call distil.

## Layout

```
paper2skills_ab_test/
├── README.md             ← this file
├── vision_adapter.py     ← simplified OpenRouter/GPT-4o vision pipeline
├── template_out/
│   ├── 10.1186_s13059-014-0550-8/SKILL.md   (DESeq2, Love et al. 2014)
│   └── 10.1186_s12859-016-0950-8/SKILL.md   (MethPat, Wong et al. 2016 *)
├── vision_out/
│   ├── 10.1186_s13059-014-0550-8/
│   │   ├── SKILL.md
│   │   └── run_manifest.json
│   └── 10.1186_s12859-016-0950-8/
│       ├── SKILL.md
│       └── run_manifest.json
├── comparison.md         ← side-by-side analysis + verdict
└── _STATUS.md
```

`*` Note on DOI `10.1186/s12859-016-0950-8`: the workspace's
`workflow_literature_map.json` claims this DOI is "systemPipeR" for
`tgirke-systempiperdata-rnaseq-finish`, but the downloaded PDF — and
both Crossref and the paper's own first page — identify it as the
**MethPat** paper (Wong et al., BMC Bioinformatics 2016). This is a
mislabel in the mapping, not a bug here. The vision method catches
this mismatch by reading the paper; the template method does not. See
`comparison.md`.

## How to reproduce

```bash
cd main/paper_primary_benchmark

# Template
python3 literature/tools/paper_to_skill.py \
  --pdf literature/pdfs/10.1186_s13059-014-0550-8.pdf \
  --out-skill-dir experiments/paper2skills_ab_test/template_out/10.1186_s13059-014-0550-8 \
  --max-pages 16

# Vision adapter (needs openrouterkey.txt or OPENROUTER_API_KEY)
python3 experiments/paper2skills_ab_test/vision_adapter.py \
  --pdf literature/pdfs/10.1186_s13059-014-0550-8.pdf \
  --out-dir experiments/paper2skills_ab_test/vision_out/10.1186_s13059-014-0550-8 \
  --pages 8 --dpi 130
```
