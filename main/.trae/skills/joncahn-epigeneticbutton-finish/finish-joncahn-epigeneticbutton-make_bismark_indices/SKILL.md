---
name: finish-joncahn-epigeneticbutton-make_bismark_indices
description: Use this skill when orchestrating the retained "make_bismark_indices" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make bismark indices stage tied to upstream `all_rna` and the downstream handoff to `bismark_map_pe`. It tracks completion via `results/finish/make_bismark_indices.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_bismark_indices
  step_name: make bismark indices
---

# Scope
Use this skill only for the `make_bismark_indices` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `all_rna`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_bismark_indices.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_bismark_indices.done`
- Representative outputs: `results/finish/make_bismark_indices.done`
- Execution targets: `make_bismark_indices`
- Downstream handoff: `bismark_map_pe`

## Guardrails
- Treat `results/finish/make_bismark_indices.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_bismark_indices.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bismark_map_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_bismark_indices.done` exists and `bismark_map_pe` can proceed without re-running make bismark indices.
