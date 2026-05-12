# Subagent G3-C status — V3 insight-oriented evaluator

Deliverables for the V3 "insight-oriented" extension of the lenient V2
evaluator. V2 and V1 evaluators are **unchanged**; V3 is strictly
additive.

## Deliverables

| path | purpose |
|------|---------|
| `ldp_r_task_eval/tools/evaluate_real_run_v3.py` | V3 CLI; imports V2 in-process, adds insight layer, emits `<batch>.v3.json` + `<batch>.v3.md` |
| `ldp_r_task_eval/tools/evaluators/insight.py` | failure-mode classifier + differential diff + confidence + actionable fix |
| `ldp_r_task_eval/tools/evaluators/skill_tokens.py` | deterministic token extractor + builder for `skill_tokens_v3.json` |
| `ldp_r_task_eval/tools/evaluators/skill_tokens_v3.json` | `{task_id → {arm → [tokens]}}` regenerated from the three live skill manifests |
| `ldp_r_task_eval/tools/EVALUATION_V3.md` | rubric + failure-mode catalog |
| `ldp_r_task_eval/runs/_evaluations/sweep_v3_<arm>_20260416T194356Z.v3.json` | V3 annotated summary per arm (×4) |
| `ldp_r_task_eval/runs/_evaluations/sweep_v3_<arm>_20260416T194356Z.v3.md` | V3 markdown per arm (×4) |
| `experiments/llm_skill_ablation/INSIGHTS_REPORT.md` | cross-arm analysis |
| `experiments/llm_skill_ablation/tools/build_insights_report.py` | deterministic report generator |

## What V3 adds on top of V2

For each task the insight block carries:

1. **Failure-mode classification** (11-way enum: `ok`, `no_rscript_call`,
   `rscript_crashed`, `output_missing`, `schema_drift`, `row_drift`,
   `float_drift`, `rds_semantic_gap`, `infinite_debug_loop`, `mixed`,
   `task_never_started`).
2. **Per-file differential diff** — one line ≤ 120 chars per expected
   file anchored on concrete tabular statistics (`cells 84%, rows 12%`,
   `rows 3 vs ref 12`, `byte-identical`, etc.).
3. **Skill-token attribution** — tokens from the arm's skill manifest
   that the agent actually surfaced in tool-call arguments.
4. **Actionable fix** — one-line remediation suggestion keyed on
   failure mode (and pulling the last R error snippet for
   `rscript_crashed`).
5. **Confidence grade** — `high` / `medium` / `low` based on whether
   the top tier was `byte_identical`, a high-fraction tabular match,
   or a sidecar fallback.

All deterministic; no LLM judge; no new third-party dependencies.

## Coverage

Ran V3 with `--insight-only` against all four V3 batch ids and produced:

| arm | `pass` | `ok` | other modes (top) |
|-----|-------:|-----:|-------------------|
| `none` | 19 | 19 | row_drift=6, rscript_crashed=4, schema_drift=2, mixed=1 |
| `paper` | 5 | 5 | task_never_started=23 (OpenRouter 402), rscript_crashed=2, row_drift=2 |
| `pipeline` | 17 | 17 | row_drift=5, schema_drift=5, rscript_crashed=4, **infinite_debug_loop=1** |
| `llm_plan` | 17 | 17 | rscript_crashed=6, schema_drift=4, row_drift=3, mixed=1, **float_drift=1** |

Total `(arm, task)` pairs classified: **128** (4 arms × 32 tasks).

## Skill-token attribution averages

| arm | tokens available | tokens matched | coverage |
|-----|-----------------:|---------------:|---------:|
| `none`     |  0.0 |  0.00 |   0.0 % |
| `paper`    |  0.4 |  0.16 |   5.2 % |
| `pipeline` | 30.2 |  2.97 |   9.9 % |
| `llm_plan` | 13.6 | 11.84 |  87.9 % |

The paper arm emits almost no code-actionable tokens (vision-adapter
output is prose); `llm_plan` emits few but highly-specific tokens which
the agent copies nearly verbatim.

## Most interesting cross-arm insight

> **`methylkit2tibble_split` — the pipeline skill actively *hurt* the
> agent.** `none` produces `row_drift` (partial content match, score
> 0.69). `pipeline` triggers `infinite_debug_loop`: the agent retries
> 7 times after its first write and burns the step budget without ever
> reaching a correct output (score 0.65). `llm_plan` takes the alternate
> path `rscript_crashed` with a concrete error ("`unused argument
> (mCpG)`" inside `dplyr::select`). Same task, three distinct failure
> archetypes, one of which is a *regression* caused by the skill
> itself. This is exactly the kind of diagnosis the V2 `overall_score`
> alone (`0.65 / 0.69 / 0.23`) cannot surface — and it is the kind of
> story a publication needs.

A close runner-up: `methylkit_filt_norm` — both `none` and `pipeline`
crash (`percMethylation` for `methylBaseDB`), but `llm_plan` passes
cleanly (`ok`, score 0.99). The *LLM-plan* skill knew to extract the
methylBase object before calling `percMethylation`; the paper and
pipeline skills did not teach that step.

## Reproduce

```bash
# Regenerate the skill-tokens map from the three live manifests
python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/evaluators/skill_tokens.py

# Score all four arms (insight-only reuses the cached <batch>.v2.json)
python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/evaluate_real_run_v3.py \
    --batch-run-id sweep_v3_none_20260416T194356Z \
    --batch-run-id sweep_v3_paper_20260416T194356Z \
    --batch-run-id sweep_v3_pipeline_20260416T194356Z \
    --batch-run-id sweep_v3_llm_plan_20260416T194356Z \
    --insight-only --quiet

# Build the cross-arm insights report
python3 main/paper_primary_benchmark/experiments/llm_skill_ablation/tools/build_insights_report.py
```
