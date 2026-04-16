---
name: finish-snakemake-workflows-star-arriba-fusion-calling-star_align
description: Use this skill when orchestrating the retained "star_align" step of the snakemake workflows star arriba fusion calling finish finish workflow. It keeps the star align stage tied to upstream `star_index` and the downstream handoff to `arriba`. It tracks completion via `results/finish/star_align.done`.
metadata:
  workflow_id: star-arriba-fusion-calling-finish
  workflow_name: snakemake workflows star arriba fusion calling finish
  step_id: star_align
  step_name: star align
---

# Scope
Use this skill only for the `star_align` step in `star-arriba-fusion-calling-finish`.

## Orchestration
- Upstream requirements: `star_index`
- Step file: `finish/star-arriba-fusion-calling-finish/steps/star_align.smk`
- Config file: `finish/star-arriba-fusion-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/star_align.done`
- Representative outputs: `results/finish/star_align.done`
- Execution targets: `star_align`
- Downstream handoff: `arriba`

## Guardrails
- Treat `results/finish/star_align.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/star_align.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `arriba` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/star_align.done` exists and `arriba` can proceed without re-running star align.
