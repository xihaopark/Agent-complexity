---
name: finish-joncahn-epigeneticbutton-make_coverage_atac
description: Use this skill when orchestrating the retained "make_coverage_atac" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make coverage atac stage tied to upstream `calling_peaks_atac` and the downstream handoff to `all_atac`. It tracks completion via `results/finish/make_coverage_atac.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_coverage_atac
  step_name: make coverage atac
---

# Scope
Use this skill only for the `make_coverage_atac` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `calling_peaks_atac`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_coverage_atac.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_coverage_atac.done`
- Representative outputs: `results/finish/make_coverage_atac.done`
- Execution targets: `make_coverage_atac`
- Downstream handoff: `all_atac`

## Guardrails
- Treat `results/finish/make_coverage_atac.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_coverage_atac.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all_atac` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_coverage_atac.done` exists and `all_atac` can proceed without re-running make coverage atac.
