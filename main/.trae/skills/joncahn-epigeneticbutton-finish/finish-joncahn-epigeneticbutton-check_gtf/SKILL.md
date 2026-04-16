---
name: finish-joncahn-epigeneticbutton-check_gtf
description: Use this skill when orchestrating the retained "check_gtf" step of the joncahn epigeneticbutton finish finish workflow. It keeps the check gtf stage tied to upstream `check_gff` and the downstream handoff to `check_chrom_sizes`. It tracks completion via `results/finish/check_gtf.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: check_gtf
  step_name: check gtf
---

# Scope
Use this skill only for the `check_gtf` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `check_gff`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/check_gtf.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/check_gtf.done`
- Representative outputs: `results/finish/check_gtf.done`
- Execution targets: `check_gtf`
- Downstream handoff: `check_chrom_sizes`

## Guardrails
- Treat `results/finish/check_gtf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/check_gtf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `check_chrom_sizes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/check_gtf.done` exists and `check_chrom_sizes` can proceed without re-running check gtf.
