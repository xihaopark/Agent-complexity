---
name: finish-tgirke-systempiperdata-varseq-plot_variant
description: Use this skill when orchestrating the retained "plot_variant" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the plot variant stage tied to upstream `venn_diagram` and the downstream handoff to `non_syn_vars`. It tracks completion via `results/finish/plot_variant.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: plot_variant
  step_name: plot variant
---

# Scope
Use this skill only for the `plot_variant` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `venn_diagram`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/plot_variant.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/plot_variant.done`
- Representative outputs: `results/finish/plot_variant.done`
- Execution targets: `plot_variant`
- Downstream handoff: `non_syn_vars`

## Guardrails
- Treat `results/finish/plot_variant.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/plot_variant.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `non_syn_vars` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/plot_variant.done` exists and `non_syn_vars` can proceed without re-running plot variant.
