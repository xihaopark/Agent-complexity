---
name: finish-joncahn-epigeneticbutton-prep_region_file
description: Use this skill when orchestrating the retained "prep_region_file" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prep region file stage tied to upstream `check_chrom_sizes` and the downstream handoff to `check_te_file`. It tracks completion via `results/finish/prep_region_file.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prep_region_file
  step_name: prep region file
---

# Scope
Use this skill only for the `prep_region_file` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `check_chrom_sizes`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prep_region_file.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prep_region_file.done`
- Representative outputs: `results/finish/prep_region_file.done`
- Execution targets: `prep_region_file`
- Downstream handoff: `check_te_file`

## Guardrails
- Treat `results/finish/prep_region_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prep_region_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `check_te_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prep_region_file.done` exists and `check_te_file` can proceed without re-running prep region file.
