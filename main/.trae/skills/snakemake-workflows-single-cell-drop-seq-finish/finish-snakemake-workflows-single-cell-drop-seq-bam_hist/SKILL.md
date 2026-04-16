---
name: finish-snakemake-workflows-single-cell-drop-seq-bam_hist
description: Use this skill when orchestrating the retained "bam_hist" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the bam hist stage tied to upstream `bead_errors_metrics` and the downstream handoff to `plot_yield`. It tracks completion via `results/finish/bam_hist.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: bam_hist
  step_name: bam hist
---

# Scope
Use this skill only for the `bam_hist` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `bead_errors_metrics`
- Step file: `finish/single-cell-drop-seq-finish/steps/bam_hist.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_hist.done`
- Representative outputs: `results/finish/bam_hist.done`
- Execution targets: `bam_hist`
- Downstream handoff: `plot_yield`

## Guardrails
- Treat `results/finish/bam_hist.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_hist.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_yield` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_hist.done` exists and `plot_yield` can proceed without re-running bam hist.
