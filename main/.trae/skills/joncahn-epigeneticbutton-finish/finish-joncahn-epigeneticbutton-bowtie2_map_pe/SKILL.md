---
name: finish-joncahn-epigeneticbutton-bowtie2_map_pe
description: Use this skill when orchestrating the retained "bowtie2_map_pe" step of the joncahn epigeneticbutton finish finish workflow. It keeps the bowtie2 map pe stage tied to upstream `make_bt2_indices` and the downstream handoff to `bowtie2_map_se`. It tracks completion via `results/finish/bowtie2_map_pe.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: bowtie2_map_pe
  step_name: bowtie2 map pe
---

# Scope
Use this skill only for the `bowtie2_map_pe` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_bt2_indices`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/bowtie2_map_pe.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bowtie2_map_pe.done`
- Representative outputs: `results/finish/bowtie2_map_pe.done`
- Execution targets: `bowtie2_map_pe`
- Downstream handoff: `bowtie2_map_se`

## Guardrails
- Treat `results/finish/bowtie2_map_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bowtie2_map_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bowtie2_map_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bowtie2_map_pe.done` exists and `bowtie2_map_se` can proceed without re-running bowtie2 map pe.
