---
name: finish-joncahn-epigeneticbutton-make_star_indices
description: Use this skill when orchestrating the retained "make_STAR_indices" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make STAR indices stage tied to upstream `all_atac` and the downstream handoff to `STAR_map_pe`. It tracks completion via `results/finish/make_STAR_indices.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_STAR_indices
  step_name: make STAR indices
---

# Scope
Use this skill only for the `make_STAR_indices` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `all_atac`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_STAR_indices.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_STAR_indices.done`
- Representative outputs: `results/finish/make_STAR_indices.done`
- Execution targets: `make_STAR_indices`
- Downstream handoff: `STAR_map_pe`

## Guardrails
- Treat `results/finish/make_STAR_indices.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_STAR_indices.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `STAR_map_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_STAR_indices.done` exists and `STAR_map_pe` can proceed without re-running make STAR indices.
