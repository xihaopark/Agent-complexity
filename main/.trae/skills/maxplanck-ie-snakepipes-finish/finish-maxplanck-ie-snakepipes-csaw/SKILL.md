---
name: finish-maxplanck-ie-snakepipes-csaw
description: Use this skill when orchestrating the retained "CSAW" step of the maxplanck ie snakepipes finish finish workflow. It keeps the CSAW stage tied to upstream `MACS2_peak_qc` and the downstream handoff to `calc_matrix_log2r_CSAW`. It tracks completion via `results/finish/CSAW.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: CSAW
  step_name: CSAW
---

# Scope
Use this skill only for the `CSAW` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `MACS2_peak_qc`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/CSAW.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/CSAW.done`
- Representative outputs: `results/finish/CSAW.done`
- Execution targets: `CSAW`
- Downstream handoff: `calc_matrix_log2r_CSAW`

## Guardrails
- Treat `results/finish/CSAW.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/CSAW.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `calc_matrix_log2r_CSAW` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/CSAW.done` exists and `calc_matrix_log2r_CSAW` can proceed without re-running CSAW.
