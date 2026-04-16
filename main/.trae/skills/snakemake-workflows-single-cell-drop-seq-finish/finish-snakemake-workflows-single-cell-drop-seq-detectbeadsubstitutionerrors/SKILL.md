---
name: finish-snakemake-workflows-single-cell-drop-seq-detectbeadsubstitutionerrors
description: Use this skill when orchestrating the retained "DetectBeadSubstitutionErrors" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the DetectBeadSubstitutionErrors stage tied to upstream `TagReadWithGeneExon` and the downstream handoff to `bead_errors_metrics`. It tracks completion via `results/finish/DetectBeadSubstitutionErrors.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: DetectBeadSubstitutionErrors
  step_name: DetectBeadSubstitutionErrors
---

# Scope
Use this skill only for the `DetectBeadSubstitutionErrors` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `TagReadWithGeneExon`
- Step file: `finish/single-cell-drop-seq-finish/steps/DetectBeadSubstitutionErrors.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/DetectBeadSubstitutionErrors.done`
- Representative outputs: `results/finish/DetectBeadSubstitutionErrors.done`
- Execution targets: `DetectBeadSubstitutionErrors`
- Downstream handoff: `bead_errors_metrics`

## Guardrails
- Treat `results/finish/DetectBeadSubstitutionErrors.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/DetectBeadSubstitutionErrors.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bead_errors_metrics` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/DetectBeadSubstitutionErrors.done` exists and `bead_errors_metrics` can proceed without re-running DetectBeadSubstitutionErrors.
