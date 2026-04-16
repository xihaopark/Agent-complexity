---
name: finish-snakemake-workflows-single-cell-drop-seq-make_report
description: Use this skill when orchestrating the retained "make_report" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the make report stage tied to upstream `merge` and the downstream handoff to `download_annotation`. It tracks completion via `results/finish/make_report.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: make_report
  step_name: make report
---

# Scope
Use this skill only for the `make_report` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `merge`
- Step file: `finish/single-cell-drop-seq-finish/steps/make_report.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_report.done`
- Representative outputs: `results/finish/make_report.done`
- Execution targets: `make_report`
- Downstream handoff: `download_annotation`

## Guardrails
- Treat `results/finish/make_report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_report.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_report.done` exists and `download_annotation` can proceed without re-running make report.
