---
name: finish-snakemake-workflows-single-cell-rna-seq-all_qc
description: Use this skill when orchestrating the retained "all_qc" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the all qc stage and the downstream handoff to `load_counts`. It tracks completion via `results/finish/all_qc.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: all_qc
  step_name: all qc
---

# Scope
Use this skill only for the `all_qc` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/single-cell-rna-seq-finish/steps/all_qc.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all_qc.done`
- Representative outputs: `results/finish/all_qc.done`
- Execution targets: `all_qc`
- Downstream handoff: `load_counts`

## Guardrails
- Treat `results/finish/all_qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all_qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `load_counts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/all_qc.done` exists and `load_counts` can proceed without re-running all qc.
