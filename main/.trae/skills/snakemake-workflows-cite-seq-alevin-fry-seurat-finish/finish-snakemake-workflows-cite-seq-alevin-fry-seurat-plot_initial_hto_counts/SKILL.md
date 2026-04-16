---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-plot_initial_hto_counts
description: Use this skill when orchestrating the retained "plot_initial_hto_counts" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the plot initial hto counts stage tied to upstream `seurat` and the downstream handoff to `filter_normalize_demux`. It tracks completion via `results/finish/plot_initial_hto_counts.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: plot_initial_hto_counts
  step_name: plot initial hto counts
---

# Scope
Use this skill only for the `plot_initial_hto_counts` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `seurat`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/plot_initial_hto_counts.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_initial_hto_counts.done`
- Representative outputs: `results/finish/plot_initial_hto_counts.done`
- Execution targets: `plot_initial_hto_counts`
- Downstream handoff: `filter_normalize_demux`

## Guardrails
- Treat `results/finish/plot_initial_hto_counts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_initial_hto_counts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_normalize_demux` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_initial_hto_counts.done` exists and `filter_normalize_demux` can proceed without re-running plot initial hto counts.
