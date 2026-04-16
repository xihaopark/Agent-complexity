---
name: finish-snakemake-workflows-single-cell-rna-seq-qc
description: Use this skill when orchestrating the retained "qc" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the qc stage tied to upstream `load_counts` and the downstream handoff to `explained_variance`. It tracks completion via `results/finish/qc.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: qc
  step_name: qc
---

# Scope
Use this skill only for the `qc` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `load_counts`
- Step file: `finish/single-cell-rna-seq-finish/steps/qc.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/qc.done`
- Representative outputs: `results/finish/qc.done`
- Execution targets: `qc`
- Downstream handoff: `explained_variance`

## Guardrails
- Treat `results/finish/qc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/qc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `explained_variance` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/qc.done` exists and `explained_variance` can proceed without re-running qc.
