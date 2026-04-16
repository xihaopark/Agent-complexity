---
name: finish-snakemake-workflows-single-cell-drop-seq-create_dict
description: Use this skill when orchestrating the retained "create_dict" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the create dict stage tied to upstream `curate_annotation` and the downstream handoff to `reduce_gtf`. It tracks completion via `results/finish/create_dict.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: create_dict
  step_name: create dict
---

# Scope
Use this skill only for the `create_dict` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `curate_annotation`
- Step file: `finish/single-cell-drop-seq-finish/steps/create_dict.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_dict.done`
- Representative outputs: `results/finish/create_dict.done`
- Execution targets: `create_dict`
- Downstream handoff: `reduce_gtf`

## Guardrails
- Treat `results/finish/create_dict.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_dict.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `reduce_gtf` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_dict.done` exists and `reduce_gtf` can proceed without re-running create dict.
