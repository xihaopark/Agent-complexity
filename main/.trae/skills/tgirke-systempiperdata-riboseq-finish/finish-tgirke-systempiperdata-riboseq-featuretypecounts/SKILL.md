---
name: finish-tgirke-systempiperdata-riboseq-featuretypecounts
description: Use this skill when orchestrating the retained "featuretypeCounts" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the featuretypeCounts stage tied to upstream `genFeatures` and the downstream handoff to `featuretypeCounts_length`. It tracks completion via `results/finish/featuretypeCounts.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: featuretypeCounts
  step_name: featuretypeCounts
---

# Scope
Use this skill only for the `featuretypeCounts` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `genFeatures`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/featuretypeCounts.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/featuretypeCounts.done`
- Representative outputs: `results/finish/featuretypeCounts.done`
- Execution targets: `featuretypeCounts`
- Downstream handoff: `featuretypeCounts_length`

## Guardrails
- Treat `results/finish/featuretypeCounts.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/featuretypeCounts.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `featuretypeCounts_length` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/featuretypeCounts.done` exists and `featuretypeCounts_length` can proceed without re-running featuretypeCounts.
