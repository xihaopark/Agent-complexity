---
name: finish-tgirke-systempiperdata-spscrna-wf_session
description: Use this skill when orchestrating the retained "wf_session" step of the tgirke systempiperdata spscrna finish finish workflow. It keeps the wf session stage tied to upstream `label_cell_type`. It tracks completion via `results/finish/wf_session.done`.
metadata:
  workflow_id: tgirke-systempiperdata-spscrna-finish
  workflow_name: tgirke systempiperdata spscrna finish
  step_id: wf_session
  step_name: wf session
---

# Scope
Use this skill only for the `wf_session` step in `tgirke-systempiperdata-spscrna-finish`.

## Orchestration
- Upstream requirements: `label_cell_type`
- Step file: `finish/tgirke-systempiperdata-spscrna-finish/steps/wf_session.smk`
- Config file: `finish/tgirke-systempiperdata-spscrna-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/wf_session.done`
- Representative outputs: `results/finish/wf_session.done`
- Execution targets: `wf_session`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/wf_session.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/wf_session.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/wf_session.done` exists and matches the intended step boundary.
