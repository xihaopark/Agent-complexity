---
name: finish-snakemake-workflows-single-cell-drop-seq-bead_errors_metrics
description: Use this skill when orchestrating the retained "bead_errors_metrics" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the bead errors metrics stage tied to upstream `DetectBeadSubstitutionErrors` and the downstream handoff to `bam_hist`. It tracks completion via `results/finish/bead_errors_metrics.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: bead_errors_metrics
  step_name: bead errors metrics
---

# Scope
Use this skill only for the `bead_errors_metrics` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `DetectBeadSubstitutionErrors`
- Step file: `finish/single-cell-drop-seq-finish/steps/bead_errors_metrics.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bead_errors_metrics.done`
- Representative outputs: `results/finish/bead_errors_metrics.done`
- Execution targets: `bead_errors_metrics`
- Downstream handoff: `bam_hist`

## Guardrails
- Treat `results/finish/bead_errors_metrics.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bead_errors_metrics.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam_hist` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bead_errors_metrics.done` exists and `bam_hist` can proceed without re-running bead errors metrics.
