---
name: finish-joncahn-epigeneticbutton-calling_peaks_atac
description: Use this skill when orchestrating the retained "calling_peaks_atac" step of the joncahn epigeneticbutton finish finish workflow. It keeps the calling peaks atac stage tied to upstream `atac_bam_to_bed` and the downstream handoff to `make_coverage_atac`. It tracks completion via `results/finish/calling_peaks_atac.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: calling_peaks_atac
  step_name: calling peaks atac
---

# Scope
Use this skill only for the `calling_peaks_atac` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `atac_bam_to_bed`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/calling_peaks_atac.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/calling_peaks_atac.done`
- Representative outputs: `results/finish/calling_peaks_atac.done`
- Execution targets: `calling_peaks_atac`
- Downstream handoff: `make_coverage_atac`

## Guardrails
- Treat `results/finish/calling_peaks_atac.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/calling_peaks_atac.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_coverage_atac` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/calling_peaks_atac.done` exists and `make_coverage_atac` can proceed without re-running calling peaks atac.
