---
name: finish-joncahn-epigeneticbutton-atac_shift_bam
description: Use this skill when orchestrating the retained "atac_shift_bam" step of the joncahn epigeneticbutton finish finish workflow. It keeps the atac shift bam stage tied to upstream `all_chip` and the downstream handoff to `atac_bam_to_bed`. It tracks completion via `results/finish/atac_shift_bam.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: atac_shift_bam
  step_name: atac shift bam
---

# Scope
Use this skill only for the `atac_shift_bam` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `all_chip`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/atac_shift_bam.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/atac_shift_bam.done`
- Representative outputs: `results/finish/atac_shift_bam.done`
- Execution targets: `atac_shift_bam`
- Downstream handoff: `atac_bam_to_bed`

## Guardrails
- Treat `results/finish/atac_shift_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/atac_shift_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `atac_bam_to_bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/atac_shift_bam.done` exists and `atac_bam_to_bed` can proceed without re-running atac shift bam.
