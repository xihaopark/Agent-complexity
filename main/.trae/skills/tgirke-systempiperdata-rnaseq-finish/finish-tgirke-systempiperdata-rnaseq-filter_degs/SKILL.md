---
name: finish-tgirke-systempiperdata-rnaseq-filter_degs
description: Use this skill when orchestrating the retained "filter_degs" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the filter degs stage tied to upstream `custom_annot` and the downstream handoff to `venn_diagram`. It tracks completion via `results/finish/filter_degs.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: filter_degs
  step_name: filter degs
---

# Scope
Use this skill only for the `filter_degs` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `custom_annot`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/filter_degs.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_degs.done`
- Representative outputs: `results/finish/filter_degs.done`
- Execution targets: `filter_degs`
- Downstream handoff: `venn_diagram`

## Guardrails
- Treat `results/finish/filter_degs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_degs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `venn_diagram` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_degs.done` exists and `venn_diagram` can proceed without re-running filter degs.
