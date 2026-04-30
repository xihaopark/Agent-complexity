# Skill-Source Router — Status (Subagent D2)

Generated: 2026-04-17 (UTC). Phase 2 of `COORDINATION_PLAN_V2.md`.

Scope:
1. Batch-run the LLM-plan generator across the final 6-task registry.
2. Extend `ldp_r_task_eval/batch_runner.py` so it accepts
   `--skill-source {none,paper,pipeline,llm_plan}` and routes the injection
   accordingly.
3. Smoke-test all 4 arms on `akinyi_deseq2`.

## 1. LLM-plan batch generation

Command:

```bash
export OPENROUTER_API_KEY="$(cat openrouterkey.txt)"
python3 main/paper_primary_benchmark/experiments/skills_llm_plan/tools/generate_llm_plan_skill.py \
  --registry main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.json \
  --out-root main/paper_primary_benchmark/experiments/skills_llm_plan
```

Result: 6/6 tasks → `experiments/skills_llm_plan/<task_id>/SKILL.md` +
`run_manifest.json`. Per-task entries rolled into
`experiments/skills_llm_plan/manifest.json::by_task_id`:
`akinyi_deseq2`, `star_deseq2_init`, `star_deseq2_contrast`, `methylkit_load`,
`methylkit_unite`, `methylkit_to_tibble`.

| task_id               | prompt_tok | completion_tok | runtime (s) | SKILL.md inline len |
|-----------------------|-----------:|---------------:|------------:|--------------------:|
| akinyi_deseq2†        | 942        | 620            | 5.66        | 2418                |
| star_deseq2_init      | 1 034      | 517            | 6.38        | 2217                |
| star_deseq2_contrast  | 1 037      | 488            | 5.72        | 1987                |
| methylkit_load        | 974        | 478            | 5.05        | 1903                |
| methylkit_unite       | 1 064      | 675            | 9.23        | 2708                |
| methylkit_to_tibble   | 1 188      | 588            | 6.18        | 2267                |
| **totals**            | **6 239**  | **3 366**      | **38.2**    | **13 500**          |

† `akinyi_deseq2`'s SKILL.md was generated during C2's Phase-1 smoke and
reused verbatim (idempotent `[skipped_exists]` in the batch log). Tokens
/ runtime shown reflect that original generation.

Cost estimate (public GPT-4o rate card, $2.50/M prompt + $10.00/M
completion): **≈ $0.0493 total** for the 6 tasks. Well under the
$0.02–$0.03 per-run line item in the budget; the bulk of the overall
$0.15 cap was reserved for smoke rollouts.

### Bug fix shipped

The batch path in `generate_llm_plan_skill.py` had a wrong `_repo_root()`
(`parents[4]` walked to `main/`, not the repo root), which caused every
task's `work_dir` resolver to fail with `Could not resolve work_dir=...`.
Fixed to `parents[5]` in this subagent's change; single-task mode was
unaffected and the tool is otherwise unchanged.

## 2. `batch_runner.py` — `--skill-source` routing

### CLI surface (new)

```text
--skill-source {none,paper,pipeline,llm_plan}   # default: none
                                                #   (or 'paper' if --skill-manifest
                                                #    is given without --skill-source,
                                                #    for back-compat with Phase 1)
--skill-manifest <path>                         # optional override;
                                                # falls back to arm default:
#   paper    -> experiments/skills/manifest.json
#   pipeline -> experiments/skills_pipeline/manifest.json
#   llm_plan -> experiments/skills_llm_plan/manifest.json
```

### Resolution logic per task (helper `_resolve_task_skill`)

1. `none` → `skill_text = _NO_SKILL_MARKER` (`"(No paper-derived skill is
   available for this task.)"`), `injected=False`.
2. `paper`, `llm_plan` → look up `manifest.by_task_id[task_id].skill_md_inline`.
3. `paper` fallback (for the 5 new V2 tasks whose `by_task_id` entry was
   never added to `experiments/skills/manifest.json`): resolve the
   registry entry's workflow id, look up `manifest.by_workflow_id[<wf>]`
   to get the DOI slug, read `experiments/skills/<doi>/SKILL.md` from
   disk, strip YAML front matter + optional ` ```markdown ` fence. This
   fallback happens in-memory only; the paper manifest on disk is **not**
   modified.
4. `pipeline` → look up `manifest.by_workflow_id[<wf>].skill_md_inline`
   only. The registry's workflow id field is detected at load time —
   tries `workflow_id`, `pipeline_workflow_id`, and `pipeline.workflow_id`
   in that order (V2 registry uses `pipeline_workflow_id`).
5. On any miss: fall back to `_NO_SKILL_MARKER`, `injected=False`,
   `reason="no_skill_for_task"`, and log a warning.

### `metadata.json::skill` schema (unified)

Always carries `arm` and `injected`. On inject, also:
`skill_sha256`, `skill_char_len`, `skill_md_path`, `lookup_field`,
`lookup_key`, `manifest_version`. Arm-specific extras:

| arm       | extra fields                                                             |
|-----------|---------------------------------------------------------------------------|
| `paper`   | `source_doi`, optional `source_tool`, `source_workflow_id`                 |
| `pipeline`| `source_workflow_id`                                                       |
| `llm_plan`| `source_task_id`, optional `source_model`                                  |
| `none`    | only `arm: "none"`, `injected: false`                                      |

### Prompt rendering (`_render_sys_prompt`)

- Unchanged behaviour for templates without `{{SKILL_MD}}` — left intact.
- For all arms, including `none`, the placeholder is substituted so the
  prompt shape is stable across arms (the `none` arm gets the
  `_NO_SKILL_MARKER` sentinel; the existing Phase 1 no-skill config also
  used this exact sentinel).

### Back-compat

Callers that still pass only `--skill-manifest <path>` (no
`--skill-source`) are treated as `--skill-source paper --skill-manifest
<that path>`, exactly matching Phase 1's behaviour.

### Resolver dry-run across all 6 tasks × 4 arms

Every (task, non-`none` arm) pair injected; no fallbacks triggered.
Workflow-keyed arms (paper-fallback, pipeline) correctly share a sha
across tasks that share a pipeline (e.g. the 3 methylation tasks →
`7a926c67…` for paper, `98666787…` for pipeline), confirming the key
detection picks up `pipeline_workflow_id` from the V2 registry.

| task_id                | paper sha256 (8) | pipeline sha256 (8) | llm_plan sha256 (8) |
|------------------------|:----------------:|:-------------------:|:-------------------:|
| akinyi_deseq2          | `482a3490`       | `4efe17fd`          | `3a889efd`          |
| star_deseq2_init       | `4aaf2fb8`       | `e9a3bc65`          | `f169268d`          |
| star_deseq2_contrast   | `4aaf2fb8`       | `e9a3bc65`          | `06cd791a`          |
| methylkit_load         | `7a926c67`       | `98666787`          | `db18cc3a`          |
| methylkit_unite        | `7a926c67`       | `98666787`          | `dc8aedc7`          |
| methylkit_to_tibble    | `7a926c67`       | `98666787`          | `0da2c673`          |

## 3. Four-arm smoke run on `akinyi_deseq2`

Shared timestamp `TS = 20260416T172519Z`. Registry used:
`registry.real.akinyi_only.json`. Config:
`experiments/llm_skill_ablation/config_llm_with_skill_v2.yaml`. Model:
`openrouter/openai/gpt-4o`, temperature 0.1, max_steps 32. Each arm ran
in its own isolated workspace copy under
`runs/batch_skill_route_smoke_<arm>_<TS>/000_akinyi_deseq2/`.

| arm      | sha256 (8) | injected | lookup                                                        | trajectory lines | evaluator verdict | byte-identical / expected |
|----------|:----------:|:--------:|---------------------------------------------------------------|:----------------:|:-----------------:|:-------------------------:|
| none     | —          | false    | —                                                             | 6                | **pass**          | 2 / 2                     |
| paper    | `482a3490` | true     | `by_task_id/akinyi_deseq2` (`experiments/skills/10.1186_s13059-016-0881-8/SKILL.md`) | 6 | **pass** | 2 / 2 |
| pipeline | `4efe17fd` | true     | `by_workflow_id/akinyi-onyango-rna_seq_pipeline-finish`        | 7                | **pass**          | 2 / 2                     |
| llm_plan | `3a889efd` | true     | `by_task_id/akinyi_deseq2` (`experiments/skills_llm_plan/akinyi_deseq2/SKILL.md`) | 8 | **pass** | 2 / 2 |

All four sha256s differ (as expected — three real skill texts + the
`_NO_SKILL_MARKER` sentinel). `metadata.json::skill.arm` is recorded
correctly in all four runs.

### Skill prompt excerpts (first ~180 chars after fold)

- **none**: `"(No paper-derived skill is available for this task.)"` (the
  shared sentinel; same text Phase 1 used).
- **paper**: `"## Method The paper provides a comprehensive review of best
  practices for RNA-seq data analysis, covering various stages from
  experimental design to advanced analysis. The core com…"` (Conesa 2016
  survey via vision adapter).
- **pipeline**: `"## Method This pipeline is designed for differential
  gene expression analysis using RNA-seq data. It processes raw FASTQ
  files through a series of steps to produce lists of differe…"` (B2's
  pipeline-skill for `akinyi-onyango-rna_seq_pipeline-finish`).
- **llm_plan**: `"## Method The task involves performing differential
  expression analysis using the DESeq2 package in R. The input is a
  featureCounts-style count matrix, and the analysis will compar…"`
  (C2's plan-as-skill; grounded in OBJECTIVE.md only).

### Evaluator outputs

Evaluator writes to `runs/_evaluations/skill_route_smoke_<arm>_<TS>.{json,md}`
(the tool does not accept `--output`, so there is no path override —
the summary is rendered directly to that folder). All four arms:

```
Tasks: 1 | pass: 1 | partial: 0 | fail: 0 | pass_rate: 100.0%
```

## 4. Manifest fallbacks observed

**None** for the 6 curated tasks. Specifically:

- `paper` arm: 1/6 resolved via `by_task_id` (only
  `akinyi_deseq2` has an explicit entry in `experiments/skills/manifest.json::by_task_id`);
  5/6 resolved via the in-memory fallback (workflow id → DOI →
  `experiments/skills/<doi>/SKILL.md`). All 6 successfully injected a
  real paper skill. No task required the `_NO_SKILL_MARKER`.
- `pipeline` arm: 6/6 resolved via `by_workflow_id` against B2's
  manifest (3 workflows × tasks: 1 akinyi, 2 star-deseq2, 3
  methylanalysis).
- `llm_plan` arm: 6/6 resolved via `by_task_id` against the manifest
  this subagent regenerated.

If anyone later drops a task whose workflow has no paper in
`experiments/skills/`, the resolver will log
`skill NOT injected: arm=... reason=no_skill_for_task`, substitute
`_NO_SKILL_MARKER` into the prompt, and continue — failing-open is the
chosen behaviour for now.

## 5. Spend accounting

- 5 new LLM-plan generations (6th was cached from C2): ~5.8 K prompt,
  ~2.7 K completion tokens → ~$0.041.
- 4 smoke rollouts on `akinyi_deseq2` (~6–8 agent steps each): OpenRouter
  invoice per Phase 1 data ≈ $0.01–$0.03 per successful rollout. Budget
  impact ≈ $0.05 – $0.10.
- **Total for this subagent: ≈ $0.09 – $0.14**, under the $0.15 cap.

## 6. Configuration / CLI reference for Subagent E

The Phase 3 sweep keeps the same config and registry, varying only
`--skill-source`. Recommended invocation (one line per arm, shared `TS`
across arms so evaluator output groups cleanly):

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
for ARM in none paper pipeline llm_plan; do
  python3 -m main.paper_primary_benchmark.ldp_r_task_eval.batch_runner \
    --registry main/paper_primary_benchmark/ldp_r_task_eval/r_tasks/registry.real.json \
    --config main/paper_primary_benchmark/experiments/llm_skill_ablation/config_llm_with_skill_v2.yaml \
    --skill-source $ARM \
    --batch-run-id sweep_skill_source_${ARM}_${TS} \
    --openrouter-key-file openrouterkey.txt
done

for ARM in none paper pipeline llm_plan; do
  python3 main/paper_primary_benchmark/ldp_r_task_eval/tools/evaluate_real_run.py \
    --batch-run-id sweep_skill_source_${ARM}_${TS}
done
```

Key notes for E:

- `--skill-source` defaults to `none`; always pass it explicitly so the
  run folder name and `metadata.json::skill.arm` line up.
- `--skill-manifest` override is rarely needed; pass only if you want to
  feed a custom manifest (e.g. rerun with the re-generated
  methylanalysis pipeline-skill at `--max-total 120000`).
- All arms use the same `config_llm_with_skill_v2.yaml`. The `{{SKILL_MD}}`
  placeholder in that config is always substituted — on `none` it gets
  the sentinel text, so prompt shape (and therefore comparable token
  counts) is stable across arms.
- Each (arm, task) pair runs in an isolated workspace copy under
  `runs/batch_<batch_run_id>/<idx>_<task_id>/workspace/`; re-running an
  arm is safe and does not mutate the canonical task workspace.
- The 6-task registry is fully paper- and pipeline-covered; the LLM-plan
  manifest also has all 6 tasks. No arm should hit a no-skill fallback
  on the curated registry.

## 7. Files touched by this subagent

- `main/paper_primary_benchmark/ldp_r_task_eval/batch_runner.py` —
  replaced single-purpose `--skill-manifest` routing with a
  `--skill-source` / `--skill-manifest` pair, added
  `_resolve_task_skill` (arm-aware), in-memory paper-manifest fallback,
  and unified `metadata.json::skill.arm` emission.
- `main/paper_primary_benchmark/experiments/skills_llm_plan/tools/generate_llm_plan_skill.py`
  — 1-line fix (`parents[4]` → `parents[5]`) so the batch registry mode
  resolves `work_dir` correctly.
- `main/paper_primary_benchmark/experiments/skills_llm_plan/<task>/{SKILL.md,run_manifest.json}`
  for the 5 new tasks (akinyi_deseq2 was already generated by C2).
- `main/paper_primary_benchmark/experiments/skills_llm_plan/manifest.json`
  — refreshed `by_task_id` with all 6 tasks.
- `runs/batch_skill_route_smoke_<arm>_20260416T172519Z/…` — 4 smoke-run
  artefact dirs.
- `runs/_evaluations/skill_route_smoke_<arm>_20260416T172519Z.{json,md}`
  — 4 evaluator summaries.

## 8. Constraints honoured

- `registry.real.json`, `evaluate_real_run.py`, and everything under
  `ldp_r_task_eval/tasks/` are untouched.
- Paper manifest (`experiments/skills/manifest.json`) is **not**
  modified; the missing `by_task_id` entries for the 5 new V2 tasks are
  handled via an in-memory fallback that reads the on-disk SKILL.md via
  the existing `by_workflow_id` → DOI mapping.
- Changes to `batch_runner.py` are additive and backwards-compatible —
  legacy `--skill-manifest <path>` invocations still behave as the
  paper arm.
- The workflow-id field is detected from the registry entry at load
  time (`workflow_id` → `pipeline_workflow_id` → `pipeline.workflow_id`);
  nothing is hard-coded to the V2 schema.
