---
name: finish-snakemake-workflows-single-cell-drop-seq-extract_all_umi_expression
description: Use this skill when orchestrating the retained "extract_all_umi_expression" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the extract all umi expression stage tied to upstream `split_bam_species` and the downstream handoff to `plot_barnyard`. It tracks completion via `results/finish/extract_all_umi_expression.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: extract_all_umi_expression
  step_name: extract all umi expression
---

# Scope
Use this skill only for the `extract_all_umi_expression` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `split_bam_species`
- Step file: `finish/single-cell-drop-seq-finish/steps/extract_all_umi_expression.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_all_umi_expression.done`
- Representative outputs: `results/finish/extract_all_umi_expression.done`
- Execution targets: `extract_all_umi_expression`
- Downstream handoff: `plot_barnyard`

## Guardrails
- Treat `results/finish/extract_all_umi_expression.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_all_umi_expression.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_barnyard` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_all_umi_expression.done` exists and `plot_barnyard` can proceed without re-running extract all umi expression.
