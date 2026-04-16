---
name: finish-snakemake-workflows-star-arriba-fusion-calling-star_index
description: Use this skill when orchestrating the retained "star_index" step of the snakemake workflows star arriba fusion calling finish finish workflow. It keeps the star index stage tied to upstream `get_genome_gtf` and the downstream handoff to `star_align`. It tracks completion via `results/finish/star_index.done`.
metadata:
  workflow_id: star-arriba-fusion-calling-finish
  workflow_name: snakemake workflows star arriba fusion calling finish
  step_id: star_index
  step_name: star index
---

# Scope
Use this skill only for the `star_index` step in `star-arriba-fusion-calling-finish`.

## Orchestration
- Upstream requirements: `get_genome_gtf`
- Step file: `finish/star-arriba-fusion-calling-finish/steps/star_index.smk`
- Config file: `finish/star-arriba-fusion-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/star_index.done`
- Representative outputs: `results/finish/star_index.done`
- Execution targets: `star_index`
- Downstream handoff: `star_align`

## Guardrails
- Treat `results/finish/star_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/star_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `star_align` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/star_index.done` exists and `star_align` can proceed without re-running star index.
