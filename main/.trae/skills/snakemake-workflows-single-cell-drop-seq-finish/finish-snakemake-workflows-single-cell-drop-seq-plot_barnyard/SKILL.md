---
name: finish-snakemake-workflows-single-cell-drop-seq-plot_barnyard
description: Use this skill when orchestrating the retained "plot_barnyard" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the plot barnyard stage tied to upstream `extract_all_umi_expression` and the downstream handoff to `extract_umi_expression_species`. It tracks completion via `results/finish/plot_barnyard.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: plot_barnyard
  step_name: plot barnyard
---

# Scope
Use this skill only for the `plot_barnyard` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `extract_all_umi_expression`
- Step file: `finish/single-cell-drop-seq-finish/steps/plot_barnyard.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_barnyard.done`
- Representative outputs: `results/finish/plot_barnyard.done`
- Execution targets: `plot_barnyard`
- Downstream handoff: `extract_umi_expression_species`

## Guardrails
- Treat `results/finish/plot_barnyard.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_barnyard.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract_umi_expression_species` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_barnyard.done` exists and `extract_umi_expression_species` can proceed without re-running plot barnyard.
