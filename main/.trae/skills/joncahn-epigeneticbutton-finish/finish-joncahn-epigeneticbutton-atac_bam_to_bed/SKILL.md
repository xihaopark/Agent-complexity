---
name: finish-joncahn-epigeneticbutton-atac_bam_to_bed
description: Use this skill when orchestrating the retained "atac_bam_to_bed" step of the joncahn epigeneticbutton finish finish workflow. It keeps the atac bam to bed stage tied to upstream `atac_shift_bam` and the downstream handoff to `calling_peaks_atac`. It tracks completion via `results/finish/atac_bam_to_bed.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: atac_bam_to_bed
  step_name: atac bam to bed
---

# Scope
Use this skill only for the `atac_bam_to_bed` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `atac_shift_bam`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/atac_bam_to_bed.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/atac_bam_to_bed.done`
- Representative outputs: `results/finish/atac_bam_to_bed.done`
- Execution targets: `atac_bam_to_bed`
- Downstream handoff: `calling_peaks_atac`

## Guardrails
- Treat `results/finish/atac_bam_to_bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/atac_bam_to_bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calling_peaks_atac` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/atac_bam_to_bed.done` exists and `calling_peaks_atac` can proceed without re-running atac bam to bed.
