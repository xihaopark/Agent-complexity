---
name: finish-snakemake-workflows-single-cell-drop-seq-summary_stats
description: Use this skill when orchestrating the retained "summary_stats" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the summary stats stage tied to upstream `violine_plots` and the downstream handoff to `create_publication_text`. It tracks completion via `results/finish/summary_stats.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: summary_stats
  step_name: summary stats
---

# Scope
Use this skill only for the `summary_stats` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `violine_plots`
- Step file: `finish/single-cell-drop-seq-finish/steps/summary_stats.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/summary_stats.done`
- Representative outputs: `results/finish/summary_stats.done`
- Execution targets: `summary_stats`
- Downstream handoff: `create_publication_text`

## Guardrails
- Treat `results/finish/summary_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/summary_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_publication_text` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/summary_stats.done` exists and `create_publication_text` can proceed without re-running summary stats.
