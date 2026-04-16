---
name: finish-akinyi-onyango-rna-seq-pipeline-quality_control
description: Use this skill when orchestrating the retained "quality_control" step of the akinyi onyango rna_seq_pipeline finish finish workflow. It keeps the quality control stage and the downstream handoff to `quality_filtering`. It tracks completion via `results/finish/quality_control.done`.
metadata:
  workflow_id: akinyi-onyango-rna_seq_pipeline-finish
  workflow_name: akinyi onyango rna_seq_pipeline finish
  step_id: quality_control
  step_name: quality control
---

# Scope
Use this skill only for the `quality_control` step in `akinyi-onyango-rna_seq_pipeline-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/akinyi-onyango-rna_seq_pipeline-finish/steps/quality_control.smk`
- Config file: `finish/akinyi-onyango-rna_seq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/quality_control.done`
- Representative outputs: `results/finish/quality_control.done`
- Execution targets: `quality_control`
- Downstream handoff: `quality_filtering`

## Guardrails
- Treat `results/finish/quality_control.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/quality_control.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `quality_filtering` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/quality_control.done` exists and `quality_filtering` can proceed without re-running quality control.
