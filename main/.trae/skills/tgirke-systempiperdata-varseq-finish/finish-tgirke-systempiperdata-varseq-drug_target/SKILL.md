---
name: finish-tgirke-systempiperdata-varseq-drug_target
description: Use this skill when orchestrating the retained "drug_target" step of the tgirke systempiperdata varseq finish finish workflow. It keeps the drug target stage tied to upstream `pathenrich` and the downstream handoff to `sessionInfo`. It tracks completion via `results/finish/drug_target.done`.
metadata:
  workflow_id: tgirke-systempiperdata-varseq-finish
  workflow_name: tgirke systempiperdata varseq finish
  step_id: drug_target
  step_name: drug target
---

# Scope
Use this skill only for the `drug_target` step in `tgirke-systempiperdata-varseq-finish`.

## Orchestration
- Upstream requirements: `pathenrich`
- Step file: `finish/tgirke-systempiperdata-varseq-finish/steps/drug_target.smk`
- Config file: `finish/tgirke-systempiperdata-varseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/drug_target.done`
- Representative outputs: `results/finish/drug_target.done`
- Execution targets: `drug_target`
- Downstream handoff: `sessionInfo`

## Guardrails
- Treat `results/finish/drug_target.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/drug_target.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sessionInfo` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/drug_target.done` exists and `sessionInfo` can proceed without re-running drug target.
