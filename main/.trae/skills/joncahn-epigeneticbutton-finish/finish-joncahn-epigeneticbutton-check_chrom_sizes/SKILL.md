---
name: finish-joncahn-epigeneticbutton-check_chrom_sizes
description: Use this skill when orchestrating the retained "check_chrom_sizes" step of the joncahn epigeneticbutton finish finish workflow. It keeps the check chrom sizes stage tied to upstream `check_gtf` and the downstream handoff to `prep_region_file`. It tracks completion via `results/finish/check_chrom_sizes.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: check_chrom_sizes
  step_name: check chrom sizes
---

# Scope
Use this skill only for the `check_chrom_sizes` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `check_gtf`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/check_chrom_sizes.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/check_chrom_sizes.done`
- Representative outputs: `results/finish/check_chrom_sizes.done`
- Execution targets: `check_chrom_sizes`
- Downstream handoff: `prep_region_file`

## Guardrails
- Treat `results/finish/check_chrom_sizes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/check_chrom_sizes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prep_region_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/check_chrom_sizes.done` exists and `prep_region_file` can proceed without re-running check chrom sizes.
