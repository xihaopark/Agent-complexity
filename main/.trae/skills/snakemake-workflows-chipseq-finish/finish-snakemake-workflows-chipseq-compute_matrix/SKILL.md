---
name: finish-snakemake-workflows-chipseq-compute_matrix
description: Use this skill when orchestrating the retained "compute_matrix" step of the snakemake workflows chipseq finish finish workflow. It keeps the compute matrix stage tied to upstream `create_igv_bigwig` and the downstream handoff to `plot_profile`. It tracks completion via `results/finish/compute_matrix.done`.
metadata:
  workflow_id: chipseq-finish
  workflow_name: snakemake workflows chipseq finish
  step_id: compute_matrix
  step_name: compute matrix
---

# Scope
Use this skill only for the `compute_matrix` step in `chipseq-finish`.

## Orchestration
- Upstream requirements: `create_igv_bigwig`
- Step file: `finish/chipseq-finish/steps/compute_matrix.smk`
- Config file: `finish/chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/compute_matrix.done`
- Representative outputs: `results/finish/compute_matrix.done`
- Execution targets: `compute_matrix`
- Downstream handoff: `plot_profile`

## Guardrails
- Treat `results/finish/compute_matrix.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/compute_matrix.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_profile` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/compute_matrix.done` exists and `plot_profile` can proceed without re-running compute matrix.
