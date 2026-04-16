---
name: finish-akinyi-onyango-rna-seq-pipeline-all
description: Use this skill when orchestrating the retained "all" step of the akinyi onyango rna_seq_pipeline finish finish workflow. It keeps the all stage tied to upstream `differential_expression`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: akinyi-onyango-rna_seq_pipeline-finish
  workflow_name: akinyi onyango rna_seq_pipeline finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `akinyi-onyango-rna_seq_pipeline-finish`.

## Orchestration
- Upstream requirements: `differential_expression`
- Step file: `finish/akinyi-onyango-rna_seq_pipeline-finish/steps/all.smk`
- Config file: `finish/akinyi-onyango-rna_seq_pipeline-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
