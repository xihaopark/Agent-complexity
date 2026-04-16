---
name: finish-akinyi-onyango-rna-seq-pipeline-generate_index
description: Use this skill when orchestrating the retained "generate_index" step of the akinyi onyango rna_seq_pipeline finish finish workflow. It keeps the generate index stage tied to upstream `qc_trimmed_files` and the downstream handoff to `read_mapping`. It tracks completion via `results/finish/generate_index.done`.
metadata:
  workflow_id: akinyi-onyango-rna_seq_pipeline-finish
  workflow_name: akinyi onyango rna_seq_pipeline finish
  step_id: generate_index
  step_name: generate index
---

# Scope
Use this skill only for the `generate_index` step in `akinyi-onyango-rna_seq_pipeline-finish`.

## Orchestration
- Upstream requirements: `qc_trimmed_files`
- Step file: `finish/akinyi-onyango-rna_seq_pipeline-finish/steps/generate_index.smk`
- Config file: `finish/akinyi-onyango-rna_seq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/generate_index.done`
- Representative outputs: `results/finish/generate_index.done`
- Execution targets: `generate_index`
- Downstream handoff: `read_mapping`

## Guardrails
- Treat `results/finish/generate_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/generate_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `read_mapping` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/generate_index.done` exists and `read_mapping` can proceed without re-running generate index.
