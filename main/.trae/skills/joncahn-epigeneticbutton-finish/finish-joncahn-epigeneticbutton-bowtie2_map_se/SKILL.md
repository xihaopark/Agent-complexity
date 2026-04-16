---
name: finish-joncahn-epigeneticbutton-bowtie2_map_se
description: Use this skill when orchestrating the retained "bowtie2_map_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the bowtie2 map se stage tied to upstream `bowtie2_map_pe` and the downstream handoff to `filter_chip_pe`. It tracks completion via `results/finish/bowtie2_map_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: bowtie2_map_se
  step_name: bowtie2 map se
---

# Scope
Use this skill only for the `bowtie2_map_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `bowtie2_map_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/bowtie2_map_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bowtie2_map_se.done`
- Representative outputs: `results/finish/bowtie2_map_se.done`
- Execution targets: `bowtie2_map_se`
- Downstream handoff: `filter_chip_pe`

## Guardrails
- Treat `results/finish/bowtie2_map_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bowtie2_map_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_chip_pe` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bowtie2_map_se.done` exists and `filter_chip_pe` can proceed without re-running bowtie2 map se.
