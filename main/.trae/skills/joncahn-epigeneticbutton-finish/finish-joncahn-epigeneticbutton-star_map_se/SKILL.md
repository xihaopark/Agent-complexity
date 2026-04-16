---
name: finish-joncahn-epigeneticbutton-star_map_se
description: Use this skill when orchestrating the retained "STAR_map_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the STAR map se stage tied to upstream `STAR_map_pe` and the downstream handoff to `filter_rna_pe`. It tracks completion via `results/finish/STAR_map_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: STAR_map_se
  step_name: STAR map se
---

# Scope
Use this skill only for the `STAR_map_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `STAR_map_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/STAR_map_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/STAR_map_se.done`
- Representative outputs: `results/finish/STAR_map_se.done`
- Execution targets: `STAR_map_se`
- Downstream handoff: `filter_rna_pe`

## Guardrails
- Treat `results/finish/STAR_map_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/STAR_map_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_rna_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/STAR_map_se.done` exists and `filter_rna_pe` can proceed without re-running STAR map se.
