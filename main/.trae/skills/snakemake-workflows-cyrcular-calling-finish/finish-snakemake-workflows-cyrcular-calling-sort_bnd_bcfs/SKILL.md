---
name: finish-snakemake-workflows-cyrcular-calling-sort_bnd_bcfs
description: Use this skill when orchestrating the retained "sort_bnd_bcfs" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the sort bnd bcfs stage tied to upstream `scatter_candidates` and the downstream handoff to `circle_bnds`. It tracks completion via `results/finish/sort_bnd_bcfs.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: sort_bnd_bcfs
  step_name: sort bnd bcfs
---

# Scope
Use this skill only for the `sort_bnd_bcfs` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `scatter_candidates`
- Step file: `finish/cyrcular-calling-finish/steps/sort_bnd_bcfs.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sort_bnd_bcfs.done`
- Representative outputs: `results/finish/sort_bnd_bcfs.done`
- Execution targets: `sort_bnd_bcfs`
- Downstream handoff: `circle_bnds`

## Guardrails
- Treat `results/finish/sort_bnd_bcfs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sort_bnd_bcfs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `circle_bnds` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sort_bnd_bcfs.done` exists and `circle_bnds` can proceed without re-running sort bnd bcfs.
