---
name: finish-snakemake-workflows-cyrcular-calling-circle_bnds
description: Use this skill when orchestrating the retained "circle_bnds" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the circle bnds stage tied to upstream `sort_bnd_bcfs` and the downstream handoff to `cyrcular_generate_tables`. It tracks completion via `results/finish/circle_bnds.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: circle_bnds
  step_name: circle bnds
---

# Scope
Use this skill only for the `circle_bnds` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `sort_bnd_bcfs`
- Step file: `finish/cyrcular-calling-finish/steps/circle_bnds.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/circle_bnds.done`
- Representative outputs: `results/finish/circle_bnds.done`
- Execution targets: `circle_bnds`
- Downstream handoff: `cyrcular_generate_tables`

## Guardrails
- Treat `results/finish/circle_bnds.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/circle_bnds.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cyrcular_generate_tables` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/circle_bnds.done` exists and `cyrcular_generate_tables` can proceed without re-running circle bnds.
