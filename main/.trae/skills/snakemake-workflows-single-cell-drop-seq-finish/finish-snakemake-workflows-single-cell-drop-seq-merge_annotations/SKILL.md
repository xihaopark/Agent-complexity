---
name: finish-snakemake-workflows-single-cell-drop-seq-merge_annotations
description: Use this skill when orchestrating the retained "merge_annotations" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the merge annotations stage tied to upstream `merge_genomes` and the downstream handoff to `curate_annotation`. It tracks completion via `results/finish/merge_annotations.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: merge_annotations
  step_name: merge annotations
---

# Scope
Use this skill only for the `merge_annotations` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `merge_genomes`
- Step file: `finish/single-cell-drop-seq-finish/steps/merge_annotations.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_annotations.done`
- Representative outputs: `results/finish/merge_annotations.done`
- Execution targets: `merge_annotations`
- Downstream handoff: `curate_annotation`

## Guardrails
- Treat `results/finish/merge_annotations.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_annotations.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `curate_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_annotations.done` exists and `curate_annotation` can proceed without re-running merge annotations.
