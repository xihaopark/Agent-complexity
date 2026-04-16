---
name: finish-snakemake-workflows-single-cell-drop-seq-curate_annotation
description: Use this skill when orchestrating the retained "curate_annotation" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the curate annotation stage tied to upstream `merge_annotations` and the downstream handoff to `create_dict`. It tracks completion via `results/finish/curate_annotation.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: curate_annotation
  step_name: curate annotation
---

# Scope
Use this skill only for the `curate_annotation` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `merge_annotations`
- Step file: `finish/single-cell-drop-seq-finish/steps/curate_annotation.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/curate_annotation.done`
- Representative outputs: `results/finish/curate_annotation.done`
- Execution targets: `curate_annotation`
- Downstream handoff: `create_dict`

## Guardrails
- Treat `results/finish/curate_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/curate_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_dict` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/curate_annotation.done` exists and `create_dict` can proceed without re-running curate annotation.
