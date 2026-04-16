---
name: finish-snakemake-workflows-single-cell-drop-seq-get_genomechrbinnbits
description: Use this skill when orchestrating the retained "get_genomeChrBinNbits" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the get genomeChrBinNbits stage tied to upstream `create_intervals` and the downstream handoff to `prep_star_index`. It tracks completion via `results/finish/get_genomeChrBinNbits.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: get_genomeChrBinNbits
  step_name: get genomeChrBinNbits
---

# Scope
Use this skill only for the `get_genomeChrBinNbits` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `create_intervals`
- Step file: `finish/single-cell-drop-seq-finish/steps/get_genomeChrBinNbits.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_genomeChrBinNbits.done`
- Representative outputs: `results/finish/get_genomeChrBinNbits.done`
- Execution targets: `get_genomeChrBinNbits`
- Downstream handoff: `prep_star_index`

## Guardrails
- Treat `results/finish/get_genomeChrBinNbits.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_genomeChrBinNbits.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prep_star_index` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_genomeChrBinNbits.done` exists and `prep_star_index` can proceed without re-running get genomeChrBinNbits.
