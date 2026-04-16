---
name: finish-snakemake-workflows-single-cell-drop-seq-convert_long_to_mtx_species
description: Use this skill when orchestrating the retained "convert_long_to_mtx_species" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the convert long to mtx species stage tied to upstream `extract_reads_expression_species` and the downstream handoff to `compress_mtx_species`. It tracks completion via `results/finish/convert_long_to_mtx_species.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: convert_long_to_mtx_species
  step_name: convert long to mtx species
---

# Scope
Use this skill only for the `convert_long_to_mtx_species` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `extract_reads_expression_species`
- Step file: `finish/single-cell-drop-seq-finish/steps/convert_long_to_mtx_species.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/convert_long_to_mtx_species.done`
- Representative outputs: `results/finish/convert_long_to_mtx_species.done`
- Execution targets: `convert_long_to_mtx_species`
- Downstream handoff: `compress_mtx_species`

## Guardrails
- Treat `results/finish/convert_long_to_mtx_species.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/convert_long_to_mtx_species.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `compress_mtx_species` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/convert_long_to_mtx_species.done` exists and `compress_mtx_species` can proceed without re-running convert long to mtx species.
