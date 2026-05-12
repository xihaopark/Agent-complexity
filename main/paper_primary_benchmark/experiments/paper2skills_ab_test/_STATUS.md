# _STATUS — Paper2Skills A/B test (Subagent B)

## Final verdict

**Recommend the vision adapter (Method 1) for the with-skill arm** of
the ldp R-task benchmark. Details + concrete system-prompt snippet in
`comparison.md`.

## Progress

- [x] Read coordination plan §B and both method implementations
      (`external/Paper2Skills/{agent,tools,prompt}.py`,
      `literature/tools/paper_to_skill.py`).
- [x] Picked two DOIs from `literature/pdfs/`:
      `10.1186_s13059-014-0550-8` (DESeq2) and
      `10.1186_s12859-016-0950-8` (mapped as systemPipeR; PDF is
      actually MethPat — see below).
- [x] Ran Method 2 (template) on both → `template_out/<doi>/SKILL.md`.
- [x] Wrote `vision_adapter.py` — OpenRouter/`openai/gpt-4o` multi-image
      distillation. Mirrors the structural intent of the original
      `external/Paper2Skills` prompt but uses a single chat-completion
      call instead of a LangGraph loop.
- [x] Ran the vision adapter on both PDFs →
      `vision_out/<doi>/{SKILL.md,run_manifest.json}`.
- [x] Wrote `comparison.md` (runtime + token cost + coverage + verdict
      + plug-in snippet).
- [x] Wrote `README.md`.

## Budget

Total Subagent B LLM spend: ~12,445 prompt + 701 completion tokens
(~$0.04 at `openai/gpt-4o` list). Two vision calls, ~27 s combined.
No attempt to install LangGraph or run `run_skill_creator.py` directly
(would have exceeded the 30-minute budget per §B of the plan).

## Blockers / notes for coordinator

1. **DOI mislabel**: `workflow_literature_map.json` lists
   `10.1186/s12859-016-0950-8` under `tgirke-systempiperdata-rnaseq-finish`
   with tool "systemPipeR". The downloaded PDF is **MethPat** (Wong et
   al., BMC Bioinformatics 2016). Please audit the mapping before Phase
   D generates skills for all 7 papers — otherwise the systemPipeR
   task will get a MethPat skill. Either replace the DOI or replace the
   PDF.
2. **Full `external/Paper2Skills` not run end-to-end.** The adapter
   gives us the data we need for Method 1 vs Method 2 comparison; if
   the project later wants runnable Python skill modules + tests, plan
   on `pipenv install` from `external/Paper2Skills/Pipfile` and a
   custom `api_type="openai"` path pointing at OpenRouter's
   `base_url="https://openrouter.ai/api/v1"`.
3. `openrouterkey.txt` is loaded from repo root by the adapter. Works.
4. No modifications made under `ldp_r_task_eval/` as required by the
   subagent brief.

## Deliverables index

- `README.md`
- `vision_adapter.py`
- `template_out/10.1186_s13059-014-0550-8/SKILL.md`
- `template_out/10.1186_s12859-016-0950-8/SKILL.md`
- `vision_out/10.1186_s13059-014-0550-8/{SKILL.md,run_manifest.json}`
- `vision_out/10.1186_s12859-016-0950-8/{SKILL.md,run_manifest.json}`
- `comparison.md`
- `_STATUS.md` (this file)
