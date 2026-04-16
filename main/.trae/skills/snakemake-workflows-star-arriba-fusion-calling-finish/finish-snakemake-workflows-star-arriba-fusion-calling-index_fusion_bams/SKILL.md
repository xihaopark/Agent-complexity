---
name: finish-snakemake-workflows-star-arriba-fusion-calling-index_fusion_bams
description: Use this skill when orchestrating the retained "index_fusion_bams" step of the snakemake workflows star arriba fusion calling finish finish workflow. It keeps the index fusion bams stage tied to upstream `arriba` and the downstream handoff to `draw_fusions`. It tracks completion via `results/finish/index_fusion_bams.done`.
metadata:
  workflow_id: star-arriba-fusion-calling-finish
  workflow_name: snakemake workflows star arriba fusion calling finish
  step_id: index_fusion_bams
  step_name: index fusion bams
---

# Scope
Use this skill only for the `index_fusion_bams` step in `star-arriba-fusion-calling-finish`.

## Orchestration
- Upstream requirements: `arriba`
- Step file: `finish/star-arriba-fusion-calling-finish/steps/index_fusion_bams.smk`
- Config file: `finish/star-arriba-fusion-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/index_fusion_bams.done`
- Representative outputs: `results/finish/index_fusion_bams.done`
- Execution targets: `index_fusion_bams`
- Downstream handoff: `draw_fusions`

## Guardrails
- Treat `results/finish/index_fusion_bams.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/index_fusion_bams.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `draw_fusions` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/index_fusion_bams.done` exists and `draw_fusions` can proceed without re-running index fusion bams.
