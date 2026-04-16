---
name: finish-joncahn-epigeneticbutton-star_map_pe
description: Use this skill when orchestrating the retained "STAR_map_pe" step of the joncahn epigeneticbutton finish finish workflow. It keeps the STAR map pe stage tied to upstream `make_STAR_indices` and the downstream handoff to `STAR_map_se`. It tracks completion via `results/finish/STAR_map_pe.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: STAR_map_pe
  step_name: STAR map pe
---

# Scope
Use this skill only for the `STAR_map_pe` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_STAR_indices`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/STAR_map_pe.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/STAR_map_pe.done`
- Representative outputs: `results/finish/STAR_map_pe.done`
- Execution targets: `STAR_map_pe`
- Downstream handoff: `STAR_map_se`

## Guardrails
- Treat `results/finish/STAR_map_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/STAR_map_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `STAR_map_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/STAR_map_pe.done` exists and `STAR_map_se` can proceed without re-running STAR map pe.
