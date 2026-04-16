---
name: finish-snakemake-workflows-single-cell-drop-seq-extract_reads_expression_species
description: Use this skill when orchestrating the retained "extract_reads_expression_species" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the extract reads expression species stage tied to upstream `extract_umi_expression_species` and the downstream handoff to `convert_long_to_mtx_species`. It tracks completion via `results/finish/extract_reads_expression_species.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: extract_reads_expression_species
  step_name: extract reads expression species
---

# Scope
Use this skill only for the `extract_reads_expression_species` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `extract_umi_expression_species`
- Step file: `finish/single-cell-drop-seq-finish/steps/extract_reads_expression_species.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_reads_expression_species.done`
- Representative outputs: `results/finish/extract_reads_expression_species.done`
- Execution targets: `extract_reads_expression_species`
- Downstream handoff: `convert_long_to_mtx_species`

## Guardrails
- Treat `results/finish/extract_reads_expression_species.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_reads_expression_species.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `convert_long_to_mtx_species` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_reads_expression_species.done` exists and `convert_long_to_mtx_species` can proceed without re-running extract reads expression species.
