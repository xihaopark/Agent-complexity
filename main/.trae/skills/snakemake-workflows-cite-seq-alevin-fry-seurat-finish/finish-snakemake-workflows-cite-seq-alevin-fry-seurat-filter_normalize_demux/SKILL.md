---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-filter_normalize_demux
description: Use this skill when orchestrating the retained "filter_normalize_demux" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the filter normalize demux stage tied to upstream `plot_initial_hto_counts` and the downstream handoff to `plot_counts_hto_filtered`. It tracks completion via `results/finish/filter_normalize_demux.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: filter_normalize_demux
  step_name: filter normalize demux
---

# Scope
Use this skill only for the `filter_normalize_demux` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `plot_initial_hto_counts`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/filter_normalize_demux.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_normalize_demux.done`
- Representative outputs: `results/finish/filter_normalize_demux.done`
- Execution targets: `filter_normalize_demux`
- Downstream handoff: `plot_counts_hto_filtered`

## Guardrails
- Treat `results/finish/filter_normalize_demux.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_normalize_demux.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_counts_hto_filtered` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_normalize_demux.done` exists and `plot_counts_hto_filtered` can proceed without re-running filter normalize demux.
