---
name: finish-snakemake-workflows-single-cell-drop-seq-merge
description: Use this skill when orchestrating the retained "merge" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the merge stage tied to upstream `extract_species` and the downstream handoff to `make_report`. It tracks completion via `results/finish/merge.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: merge
  step_name: merge
---

# Scope
Use this skill only for the `merge` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `extract_species`
- Step file: `finish/single-cell-drop-seq-finish/steps/merge.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge.done`
- Representative outputs: `results/finish/merge.done`
- Execution targets: `merge`
- Downstream handoff: `make_report`

## Guardrails
- Treat `results/finish/merge.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_report` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge.done` exists and `make_report` can proceed without re-running merge.
