---
name: finish-akinyi-onyango-rna-seq-pipeline-read_mapping
description: Use this skill when orchestrating the retained "read_mapping" step of the akinyi onyango rna_seq_pipeline finish finish workflow. It keeps the read mapping stage tied to upstream `generate_index` and the downstream handoff to `read_counts`. It tracks completion via `results/finish/read_mapping.done`.
metadata:
  workflow_id: akinyi-onyango-rna_seq_pipeline-finish
  workflow_name: akinyi onyango rna_seq_pipeline finish
  step_id: read_mapping
  step_name: read mapping
---

# Scope
Use this skill only for the `read_mapping` step in `akinyi-onyango-rna_seq_pipeline-finish`.

## Orchestration
- Upstream requirements: `generate_index`
- Step file: `finish/akinyi-onyango-rna_seq_pipeline-finish/steps/read_mapping.smk`
- Config file: `finish/akinyi-onyango-rna_seq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/read_mapping.done`
- Representative outputs: `results/finish/read_mapping.done`
- Execution targets: `read_mapping`
- Downstream handoff: `read_counts`

## Guardrails
- Treat `results/finish/read_mapping.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/read_mapping.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `read_counts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/read_mapping.done` exists and `read_counts` can proceed without re-running read mapping.
