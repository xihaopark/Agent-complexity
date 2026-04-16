---
name: finish-gustaveroussy-sopa-report
description: Use this skill when orchestrating the retained "report" step of the gustaveroussy sopa finish finish workflow. It keeps the report stage tied to upstream `explorer` and the downstream handoff to `patch_segmentation_cellpose`. It tracks completion via `results/finish/report.done`.
metadata:
  workflow_id: gustaveroussy-sopa-finish
  workflow_name: gustaveroussy sopa finish
  step_id: report
  step_name: report
---

# Scope
Use this skill only for the `report` step in `gustaveroussy-sopa-finish`.

## Orchestration
- Upstream requirements: `explorer`
- Step file: `finish/gustaveroussy-sopa-finish/steps/report.smk`
- Config file: `finish/gustaveroussy-sopa-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/report.done`
- Representative outputs: `results/finish/report.done`
- Execution targets: `report`
- Downstream handoff: `patch_segmentation_cellpose`

## Guardrails
- Treat `results/finish/report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/report.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `patch_segmentation_cellpose` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/report.done` exists and `patch_segmentation_cellpose` can proceed without re-running report.
