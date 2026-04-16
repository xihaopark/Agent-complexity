---
name: finish-akinyi-onyango-rna-seq-pipeline-quality_filtering
description: Use this skill when orchestrating the retained "quality_filtering" step of the akinyi onyango rna_seq_pipeline finish finish workflow. It keeps the quality filtering stage tied to upstream `quality_control` and the downstream handoff to `qc_trimmed_files`. It tracks completion via `results/finish/quality_filtering.done`.
metadata:
  workflow_id: akinyi-onyango-rna_seq_pipeline-finish
  workflow_name: akinyi onyango rna_seq_pipeline finish
  step_id: quality_filtering
  step_name: quality filtering
---

# Scope
Use this skill only for the `quality_filtering` step in `akinyi-onyango-rna_seq_pipeline-finish`.

## Orchestration
- Upstream requirements: `quality_control`
- Step file: `finish/akinyi-onyango-rna_seq_pipeline-finish/steps/quality_filtering.smk`
- Config file: `finish/akinyi-onyango-rna_seq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/quality_filtering.done`
- Representative outputs: `results/finish/quality_filtering.done`
- Execution targets: `quality_filtering`
- Downstream handoff: `qc_trimmed_files`

## Guardrails
- Treat `results/finish/quality_filtering.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/quality_filtering.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `qc_trimmed_files` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/quality_filtering.done` exists and `qc_trimmed_files` can proceed without re-running quality filtering.
