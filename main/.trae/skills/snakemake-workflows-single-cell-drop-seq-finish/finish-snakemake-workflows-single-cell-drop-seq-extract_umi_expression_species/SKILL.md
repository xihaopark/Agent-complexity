---
name: finish-snakemake-workflows-single-cell-drop-seq-extract_umi_expression_species
description: Use this skill when orchestrating the retained "extract_umi_expression_species" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the extract umi expression species stage tied to upstream `plot_barnyard` and the downstream handoff to `extract_reads_expression_species`. It tracks completion via `results/finish/extract_umi_expression_species.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: extract_umi_expression_species
  step_name: extract umi expression species
---

# Scope
Use this skill only for the `extract_umi_expression_species` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `plot_barnyard`
- Step file: `finish/single-cell-drop-seq-finish/steps/extract_umi_expression_species.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_umi_expression_species.done`
- Representative outputs: `results/finish/extract_umi_expression_species.done`
- Execution targets: `extract_umi_expression_species`
- Downstream handoff: `extract_reads_expression_species`

## Guardrails
- Treat `results/finish/extract_umi_expression_species.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_umi_expression_species.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract_reads_expression_species` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_umi_expression_species.done` exists and `extract_reads_expression_species` can proceed without re-running extract umi expression species.
