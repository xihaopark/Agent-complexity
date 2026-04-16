---
name: finish-maxplanck-ie-snakepipes-csaw_report
description: Use this skill when orchestrating the retained "CSAW_report" step of the maxplanck ie snakepipes finish finish workflow. It keeps the CSAW report stage tied to upstream `plot_heatmap_cov_CSAW` and the downstream handoff to `get_nearest_transcript`. It tracks completion via `results/finish/CSAW_report.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: CSAW_report
  step_name: CSAW report
---

# Scope
Use this skill only for the `CSAW_report` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `plot_heatmap_cov_CSAW`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/CSAW_report.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/CSAW_report.done`
- Representative outputs: `results/finish/CSAW_report.done`
- Execution targets: `CSAW_report`
- Downstream handoff: `get_nearest_transcript`

## Guardrails
- Treat `results/finish/CSAW_report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/CSAW_report.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_nearest_transcript` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/CSAW_report.done` exists and `get_nearest_transcript` can proceed without re-running CSAW report.
