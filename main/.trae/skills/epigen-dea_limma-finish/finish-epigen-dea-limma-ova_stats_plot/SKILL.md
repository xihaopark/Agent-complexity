---
name: finish-epigen-dea-limma-ova_stats_plot
description: Use this skill when orchestrating the retained "ova_stats_plot" step of the epigen dea_limma finish finish workflow. It keeps the ova stats plot stage tied to upstream `aggregate` and the downstream handoff to `fetch_file`. It tracks completion via `results/finish/ova_stats_plot.done`.
metadata:
  workflow_id: epigen-dea_limma-finish
  workflow_name: epigen dea_limma finish
  step_id: ova_stats_plot
  step_name: ova stats plot
---

# Scope
Use this skill only for the `ova_stats_plot` step in `epigen-dea_limma-finish`.

## Orchestration
- Upstream requirements: `aggregate`
- Step file: `finish/epigen-dea_limma-finish/steps/ova_stats_plot.smk`
- Config file: `finish/epigen-dea_limma-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ova_stats_plot.done`
- Representative outputs: `results/finish/ova_stats_plot.done`
- Execution targets: `ova_stats_plot`
- Downstream handoff: `fetch_file`

## Guardrails
- Treat `results/finish/ova_stats_plot.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ova_stats_plot.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fetch_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ova_stats_plot.done` exists and `fetch_file` can proceed without re-running ova stats plot.
