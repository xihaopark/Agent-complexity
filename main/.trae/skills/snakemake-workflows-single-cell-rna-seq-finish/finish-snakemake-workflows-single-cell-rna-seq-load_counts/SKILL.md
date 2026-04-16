---
name: finish-snakemake-workflows-single-cell-rna-seq-load_counts
description: Use this skill when orchestrating the retained "load_counts" step of the snakemake workflows single cell rna seq finish finish workflow. It keeps the load counts stage tied to upstream `all_qc` and the downstream handoff to `qc`. It tracks completion via `results/finish/load_counts.done`.
metadata:
  workflow_id: single-cell-rna-seq-finish
  workflow_name: snakemake workflows single cell rna seq finish
  step_id: load_counts
  step_name: load counts
---

# Scope
Use this skill only for the `load_counts` step in `single-cell-rna-seq-finish`.

## Orchestration
- Upstream requirements: `all_qc`
- Step file: `finish/single-cell-rna-seq-finish/steps/load_counts.smk`
- Config file: `finish/single-cell-rna-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/load_counts.done`
- Representative outputs: `results/finish/load_counts.done`
- Execution targets: `load_counts`
- Downstream handoff: `qc`

## Guardrails
- Treat `results/finish/load_counts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/load_counts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `qc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/load_counts.done` exists and `qc` can proceed without re-running load counts.
