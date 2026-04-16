---
name: finish-akinyi-onyango-rna-seq-pipeline-read_counts
description: Use this skill when orchestrating the retained "read_counts" step of the akinyi onyango rna_seq_pipeline finish finish workflow. It keeps the read counts stage tied to upstream `read_mapping` and the downstream handoff to `differential_expression`. It tracks completion via `results/finish/read_counts.done`.
metadata:
  workflow_id: akinyi-onyango-rna_seq_pipeline-finish
  workflow_name: akinyi onyango rna_seq_pipeline finish
  step_id: read_counts
  step_name: read counts
---

# Scope
Use this skill only for the `read_counts` step in `akinyi-onyango-rna_seq_pipeline-finish`.

## Orchestration
- Upstream requirements: `read_mapping`
- Step file: `finish/akinyi-onyango-rna_seq_pipeline-finish/steps/read_counts.smk`
- Config file: `finish/akinyi-onyango-rna_seq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/read_counts.done`
- Representative outputs: `results/finish/read_counts.done`
- Execution targets: `read_counts`
- Downstream handoff: `differential_expression`

## Guardrails
- Treat `results/finish/read_counts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/read_counts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `differential_expression` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/read_counts.done` exists and `differential_expression` can proceed without re-running read counts.
