---
name: finish-epigen-rnaseq-pipeline-align
description: Use this skill when orchestrating the retained "align" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the align stage tied to upstream `trim_filter` and the downstream handoff to `count_matrix`. It tracks completion via `results/finish/align.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: align
  step_name: align
---

# Scope
Use this skill only for the `align` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `trim_filter`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/align.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/align.done`
- Representative outputs: `results/finish/align.done`
- Execution targets: `align`
- Downstream handoff: `count_matrix`

## Guardrails
- Treat `results/finish/align.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/align.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `count_matrix` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/align.done` exists and `count_matrix` can proceed without re-running align.
