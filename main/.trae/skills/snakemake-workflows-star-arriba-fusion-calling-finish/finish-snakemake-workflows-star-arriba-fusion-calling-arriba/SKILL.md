---
name: finish-snakemake-workflows-star-arriba-fusion-calling-arriba
description: Use this skill when orchestrating the retained "arriba" step of the snakemake workflows star arriba fusion calling finish finish workflow. It keeps the arriba stage tied to upstream `star_align` and the downstream handoff to `index_fusion_bams`. It tracks completion via `results/finish/arriba.done`.
metadata:
  workflow_id: star-arriba-fusion-calling-finish
  workflow_name: snakemake workflows star arriba fusion calling finish
  step_id: arriba
  step_name: arriba
---

# Scope
Use this skill only for the `arriba` step in `star-arriba-fusion-calling-finish`.

## Orchestration
- Upstream requirements: `star_align`
- Step file: `finish/star-arriba-fusion-calling-finish/steps/arriba.smk`
- Config file: `finish/star-arriba-fusion-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/arriba.done`
- Representative outputs: `results/finish/arriba.done`
- Execution targets: `arriba`
- Downstream handoff: `index_fusion_bams`

## Guardrails
- Treat `results/finish/arriba.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/arriba.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `index_fusion_bams` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/arriba.done` exists and `index_fusion_bams` can proceed without re-running arriba.
