---
name: finish-akinyi-onyango-rna-seq-pipeline-qc_trimmed_files
description: Use this skill when orchestrating the retained "qc_trimmed_files" step of the akinyi onyango rna_seq_pipeline finish finish workflow. It keeps the qc trimmed files stage tied to upstream `quality_filtering` and the downstream handoff to `generate_index`. It tracks completion via `results/finish/qc_trimmed_files.done`.
metadata:
  workflow_id: akinyi-onyango-rna_seq_pipeline-finish
  workflow_name: akinyi onyango rna_seq_pipeline finish
  step_id: qc_trimmed_files
  step_name: qc trimmed files
---

# Scope
Use this skill only for the `qc_trimmed_files` step in `akinyi-onyango-rna_seq_pipeline-finish`.

## Orchestration
- Upstream requirements: `quality_filtering`
- Step file: `finish/akinyi-onyango-rna_seq_pipeline-finish/steps/qc_trimmed_files.smk`
- Config file: `finish/akinyi-onyango-rna_seq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/qc_trimmed_files.done`
- Representative outputs: `results/finish/qc_trimmed_files.done`
- Execution targets: `qc_trimmed_files`
- Downstream handoff: `generate_index`

## Guardrails
- Treat `results/finish/qc_trimmed_files.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/qc_trimmed_files.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `generate_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/qc_trimmed_files.done` exists and `generate_index` can proceed without re-running qc trimmed files.
