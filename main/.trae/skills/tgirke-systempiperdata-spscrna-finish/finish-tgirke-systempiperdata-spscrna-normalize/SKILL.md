---
name: finish-tgirke-systempiperdata-spscrna-normalize
description: Use this skill when orchestrating the retained "normalize" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the normalize stage tied to upstream `filter_cells` and the downstream handoff to `find_var_genes`. It tracks completion via `results/finish/normalize.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: normalize
  step_name: normalize
---

# Scope
Use this skill only for the `normalize` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `filter_cells`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/normalize.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/normalize.done`
- Representative outputs: `results/finish/normalize.done`
- Execution targets: `normalize`
- Downstream handoff: `find_var_genes`

## Guardrails
- Treat `results/finish/normalize.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/normalize.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `find_var_genes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/normalize.done` exists and `find_var_genes` can proceed without re-running normalize.
