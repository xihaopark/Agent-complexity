---
name: finish-snakemake-workflows-star-arriba-fusion-calling-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows star arriba fusion calling finish finish workflow. It keeps the all stage tied to upstream `draw_fusions`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: star-arriba-fusion-calling-finish
  workflow_name: snakemake workflows star arriba fusion calling finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `star-arriba-fusion-calling-finish`.

## Orchestration
- Upstream requirements: `draw_fusions`
- Step file: `finish/star-arriba-fusion-calling-finish/steps/all.smk`
- Config file: `finish/star-arriba-fusion-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
