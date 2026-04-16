---
name: finish-snakemake-workflows-star-arriba-fusion-calling-draw_fusions
description: Use this skill when orchestrating the retained "draw_fusions" step of the snakemake workflows star arriba fusion calling finish finish workflow. It keeps the draw fusions stage tied to upstream `index_fusion_bams` and the downstream handoff to `all`. It tracks completion via `results/finish/draw_fusions.done`.
metadata:
  workflow_id: star-arriba-fusion-calling-finish
  workflow_name: snakemake workflows star arriba fusion calling finish
  step_id: draw_fusions
  step_name: draw fusions
---

# Scope
Use this skill only for the `draw_fusions` step in `star-arriba-fusion-calling-finish`.

## Orchestration
- Upstream requirements: `index_fusion_bams`
- Step file: `finish/star-arriba-fusion-calling-finish/steps/draw_fusions.smk`
- Config file: `finish/star-arriba-fusion-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/draw_fusions.done`
- Representative outputs: `results/finish/draw_fusions.done`
- Execution targets: `draw_fusions`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/draw_fusions.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/draw_fusions.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/draw_fusions.done` exists and `all` can proceed without re-running draw fusions.
