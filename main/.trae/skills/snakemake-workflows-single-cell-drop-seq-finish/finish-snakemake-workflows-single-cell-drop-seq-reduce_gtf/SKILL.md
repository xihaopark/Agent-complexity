---
name: finish-snakemake-workflows-single-cell-drop-seq-reduce_gtf
description: Use this skill when orchestrating the retained "reduce_gtf" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the reduce gtf stage tied to upstream `create_dict` and the downstream handoff to `create_refFlat`. It tracks completion via `results/finish/reduce_gtf.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: reduce_gtf
  step_name: reduce gtf
---

# Scope
Use this skill only for the `reduce_gtf` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `create_dict`
- Step file: `finish/single-cell-drop-seq-finish/steps/reduce_gtf.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/reduce_gtf.done`
- Representative outputs: `results/finish/reduce_gtf.done`
- Execution targets: `reduce_gtf`
- Downstream handoff: `create_refFlat`

## Guardrails
- Treat `results/finish/reduce_gtf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/reduce_gtf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_refFlat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/reduce_gtf.done` exists and `create_refFlat` can proceed without re-running reduce gtf.
