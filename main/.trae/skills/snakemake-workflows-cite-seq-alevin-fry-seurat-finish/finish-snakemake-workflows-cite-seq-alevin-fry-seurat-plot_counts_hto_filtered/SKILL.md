---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-plot_counts_hto_filtered
description: Use this skill when orchestrating the retained "plot_counts_hto_filtered" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the plot counts hto filtered stage tied to upstream `filter_normalize_demux` and the downstream handoff to `filter_negatives`. It tracks completion via `results/finish/plot_counts_hto_filtered.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: plot_counts_hto_filtered
  step_name: plot counts hto filtered
---

# Scope
Use this skill only for the `plot_counts_hto_filtered` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `filter_normalize_demux`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/plot_counts_hto_filtered.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_counts_hto_filtered.done`
- Representative outputs: `results/finish/plot_counts_hto_filtered.done`
- Execution targets: `plot_counts_hto_filtered`
- Downstream handoff: `filter_negatives`

## Guardrails
- Treat `results/finish/plot_counts_hto_filtered.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_counts_hto_filtered.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_negatives` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_counts_hto_filtered.done` exists and `filter_negatives` can proceed without re-running plot counts hto filtered.
