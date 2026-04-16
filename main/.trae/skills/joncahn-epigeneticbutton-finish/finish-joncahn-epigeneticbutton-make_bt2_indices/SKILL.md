---
name: finish-joncahn-epigeneticbutton-make_bt2_indices
description: Use this skill when orchestrating the retained "make_bt2_indices" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make bt2 indices stage tied to upstream `get_available_bam` and the downstream handoff to `bowtie2_map_pe`. It tracks completion via `results/finish/make_bt2_indices.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_bt2_indices
  step_name: make bt2 indices
---

# Scope
Use this skill only for the `make_bt2_indices` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `get_available_bam`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_bt2_indices.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_bt2_indices.done`
- Representative outputs: `results/finish/make_bt2_indices.done`
- Execution targets: `make_bt2_indices`
- Downstream handoff: `bowtie2_map_pe`

## Guardrails
- Treat `results/finish/make_bt2_indices.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_bt2_indices.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bowtie2_map_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_bt2_indices.done` exists and `bowtie2_map_pe` can proceed without re-running make bt2 indices.
