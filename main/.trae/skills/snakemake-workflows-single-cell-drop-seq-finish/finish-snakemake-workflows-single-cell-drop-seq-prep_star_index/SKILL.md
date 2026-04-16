---
name: finish-snakemake-workflows-single-cell-drop-seq-prep_star_index
description: Use this skill when orchestrating the retained "prep_star_index" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the prep star index stage tied to upstream `get_genomeChrBinNbits` and the downstream handoff to `create_star_index`. It tracks completion via `results/finish/prep_star_index.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: prep_star_index
  step_name: prep star index
---

# Scope
Use this skill only for the `prep_star_index` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `get_genomeChrBinNbits`
- Step file: `finish/single-cell-drop-seq-finish/steps/prep_star_index.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prep_star_index.done`
- Representative outputs: `results/finish/prep_star_index.done`
- Execution targets: `prep_star_index`
- Downstream handoff: `create_star_index`

## Guardrails
- Treat `results/finish/prep_star_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prep_star_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_star_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prep_star_index.done` exists and `create_star_index` can proceed without re-running prep star index.
