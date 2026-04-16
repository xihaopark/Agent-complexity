---
name: finish-tgirke-systempiperdata-varseq-venn_diagram
description: Use this skill when orchestrating the retained "venn_diagram" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the venn diagram stage tied to upstream `plot_var_boxplot` and the downstream handoff to `plot_variant`. It tracks completion via `results/finish/venn_diagram.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: venn_diagram
  step_name: venn diagram
---

# Scope
Use this skill only for the `venn_diagram` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `plot_var_boxplot`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/venn_diagram.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/venn_diagram.done`
- Representative outputs: `results/finish/venn_diagram.done`
- Execution targets: `venn_diagram`
- Downstream handoff: `plot_variant`

## Guardrails
- Treat `results/finish/venn_diagram.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/venn_diagram.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_variant` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/venn_diagram.done` exists and `plot_variant` can proceed without re-running venn diagram.
