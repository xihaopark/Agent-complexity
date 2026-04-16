---
name: finish-tgirke-systempiperdata-spscrna-label_cell_type
description: Use this skill when orchestrating the retained "label_cell_type" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the label cell type stage tied to upstream `plot_markers` and the downstream handoff to `wf_session`. It tracks completion via `results/finish/label_cell_type.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: label_cell_type
  step_name: label cell type
---

# Scope
Use this skill only for the `label_cell_type` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `plot_markers`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/label_cell_type.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/label_cell_type.done`
- Representative outputs: `results/finish/label_cell_type.done`
- Execution targets: `label_cell_type`
- Downstream handoff: `wf_session`

## Guardrails
- Treat `results/finish/label_cell_type.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/label_cell_type.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `wf_session` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/label_cell_type.done` exists and `wf_session` can proceed without re-running label cell type.
