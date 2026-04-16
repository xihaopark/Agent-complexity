---
name: finish-tgirke-systempiperdata-rnaseq-venn_diagram
description: Use this skill when orchestrating the retained "venn_diagram" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the venn diagram stage tied to upstream `filter_degs` and the downstream handoff to `get_go_annot`. It tracks completion via `results/finish/venn_diagram.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: venn_diagram
  step_name: venn diagram
---

# Scope
Use this skill only for the `venn_diagram` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `filter_degs`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/venn_diagram.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/venn_diagram.done`
- Representative outputs: `results/finish/venn_diagram.done`
- Execution targets: `venn_diagram`
- Downstream handoff: `get_go_annot`

## Guardrails
- Treat `results/finish/venn_diagram.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/venn_diagram.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_go_annot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/venn_diagram.done` exists and `get_go_annot` can proceed without re-running venn diagram.
