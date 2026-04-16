---
name: finish-epigen-rnaseq-pipeline-check_read_type
description: Use this skill when orchestrating the retained "check_read_type" step of the epigen rnaseq_pipeline finish finish workflow. It keeps the check read type stage tied to upstream `plot_sample_annotation` and the downstream handoff to `trim_filter`. It tracks completion via `results/finish/check_read_type.done`.
metadata:
  workflow_id: epigen-rnaseq_pipeline-finish
  workflow_name: epigen rnaseq_pipeline finish
  step_id: check_read_type
  step_name: check read type
---

# Scope
Use this skill only for the `check_read_type` step in `epigen-rnaseq_pipeline-finish`.

## Orchestration
- Upstream requirements: `plot_sample_annotation`
- Step file: `finish/epigen-rnaseq_pipeline-finish/steps/check_read_type.smk`
- Config file: `finish/epigen-rnaseq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/check_read_type.done`
- Representative outputs: `results/finish/check_read_type.done`
- Execution targets: `check_read_type`
- Downstream handoff: `trim_filter`

## Guardrails
- Treat `results/finish/check_read_type.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/check_read_type.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `trim_filter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/check_read_type.done` exists and `trim_filter` can proceed without re-running check read type.
