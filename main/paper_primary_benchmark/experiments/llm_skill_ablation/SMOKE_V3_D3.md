# Smoke test V3 — D3

**Date**: 2026-04-17
**Operator**: Subagent D3

## Design

- 2 tasks selected from `registry.real.json`:
  - `methylkit_load` — full coverage (paper + pipeline + llm_plan)
  - `spilterlize_filter_features` — partial coverage (pipeline + llm_plan, no paper)
- 4 arms: `none`, `paper`, `pipeline`, `llm_plan`
- `--max-steps 2` via `config/smoke_v3_d3.yaml` (the batch_runner reads `max_steps` from the YAML config; there is no `--max-steps` CLI flag, so we expose it via YAML).
- Sys-prompt template includes `{{SKILL_MD}}` placeholder so the skill body is actually spliced into the system prompt (not just recorded in metadata).
- `--openrouter-key-file ../../openrouterkey.txt` (relative to `main/paper_primary_benchmark/`).
- Smoke registry: `ldp_r_task_eval/r_tasks/registry.smoke_v3_d3.json`.

## Commands

```bash
cd main/paper_primary_benchmark
for ARM in none paper pipeline llm_plan; do
  PYTHONPATH=.. python3 -m paper_primary_benchmark.ldp_r_task_eval.batch_runner \
    --registry ldp_r_task_eval/r_tasks/registry.smoke_v3_d3.json \
    --config ldp_r_task_eval/config/smoke_v3_d3.yaml \
    --batch-run-id smoke_v3_d3_${ARM} \
    --skill-source $ARM \
    --openrouter-key-file ../../openrouterkey.txt
done
```

## Results — `metadata.json::skill`

| arm | task | injected | skill_md_path | lookup_key | reason |
|---|---|---|---|---|---|
| none | methylkit_load | False | — | — | arm_none (implicit) |
| none | spilterlize_filter_features | False | — | — | arm_none (implicit) |
| paper | methylkit_load | **True** | `experiments/skills/10.1186_s12859-016-0950-8/SKILL.md` | methylkit_load (by_task_id) | — |
| paper | spilterlize_filter_features | **False** | — | spilterlize_filter_features | `no_skill_for_task` (graceful fallback to `_NO_SKILL_MARKER`) |
| pipeline | methylkit_load | **True** | `experiments/skills_pipeline/fritjoflammers-snakemake-methylanalysis-finish/SKILL.md` | fritjoflammers-snakemake-methylanalysis-finish | — |
| pipeline | spilterlize_filter_features | **True** | `experiments/skills_pipeline/epigen-spilterlize_integrate-finish/SKILL.md` | epigen-spilterlize_integrate-finish | — |
| llm_plan | methylkit_load | **True** | `experiments/skills_llm_plan/methylkit_load/SKILL.md` | methylkit_load | — |
| llm_plan | spilterlize_filter_features | **True** | `experiments/skills_llm_plan/spilterlize_filter_features/SKILL.md` | spilterlize_filter_features | — |

All 8 `batch_runner` invocations logged `batch finished: 2 tasks ok`. Task outputs were not expected to be correct (max_steps=2) — we only validated that the injection path resolves and the run artifacts are written.

## Graceful-failure observation

The task `spilterlize_filter_features` has no paper coverage (its workflow has `primary_doi: null`). In the `paper` arm:

- `_resolve_task_skill` returned `(_NO_SKILL_MARKER, {"arm":"paper","injected":false,"reason":"no_skill_for_task","manifest_version":3,"lookup_field":"by_task_id","lookup_key":"spilterlize_filter_features"})`.
- `_render_sys_prompt` substituted the `{{SKILL_MD}}` placeholder with `(No paper-derived skill is available for this task.)`, keeping prompt shape stable.
- `batch_runner.main_async` did NOT crash: the run still executed through the agent and wrote `metadata.json` / `trajectory.jsonl`.
- The log line recorded was:
  `skill NOT injected: arm=paper task=spilterlize_filter_features reason=no_skill_for_task`

So the paper arm fails gracefully for paperless workflows without requiring changes to `batch_runner.py`. E3 can safely run all 32 × 4 combinations; it will produce `injected=false` records for the 14 paperless tasks in the paper arm instead of aborting.

## Sanity check: all 4 arms actually spliced different system prompts

The `skill_sha256` values in `metadata.json::skill` are distinct across injected arms, proving the prompt differs per arm:

- `paper`/methylkit_load → `7a926c67d6...`
- `pipeline`/methylkit_load → `5df053f68e...`
- `llm_plan`/methylkit_load → `db18cc3a9c...`

## Artifacts

- `ldp_r_task_eval/runs/batch_smoke_v3_d3_none/`
- `ldp_r_task_eval/runs/batch_smoke_v3_d3_paper/`
- `ldp_r_task_eval/runs/batch_smoke_v3_d3_pipeline/`
- `ldp_r_task_eval/runs/batch_smoke_v3_d3_llm_plan/`
