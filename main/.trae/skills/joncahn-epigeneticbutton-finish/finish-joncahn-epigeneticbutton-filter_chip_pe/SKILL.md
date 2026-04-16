---
name: finish-joncahn-epigeneticbutton-filter_chip_pe
description: Use this skill when orchestrating the retained "filter_chip_pe" step of the joncahn epigeneticbutton finish finish workflow. It keeps the filter chip pe stage tied to upstream `bowtie2_map_se` and the downstream handoff to `filter_chip_se`. It tracks completion via `results/finish/filter_chip_pe.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: filter_chip_pe
  step_name: filter chip pe
---

# Scope
Use this skill only for the `filter_chip_pe` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `bowtie2_map_se`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/filter_chip_pe.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_chip_pe.done`
- Representative outputs: `results/finish/filter_chip_pe.done`
- Execution targets: `filter_chip_pe`
- Downstream handoff: `filter_chip_se`

## Guardrails
- Treat `results/finish/filter_chip_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_chip_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_chip_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_chip_pe.done` exists and `filter_chip_se` can proceed without re-running filter chip pe.
