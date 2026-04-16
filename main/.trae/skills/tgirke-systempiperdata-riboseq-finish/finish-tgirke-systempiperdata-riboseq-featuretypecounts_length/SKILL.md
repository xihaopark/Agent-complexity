---
name: finish-tgirke-systempiperdata-riboseq-featuretypecounts_length
description: Use this skill when orchestrating the retained "featuretypeCounts_length" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the featuretypeCounts length stage tied to upstream `featuretypeCounts` and the downstream handoff to `pred_ORF`. It tracks completion via `results/finish/featuretypeCounts_length.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: featuretypeCounts_length
  step_name: featuretypeCounts length
---

# Scope
Use this skill only for the `featuretypeCounts_length` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `featuretypeCounts`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/featuretypeCounts_length.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/featuretypeCounts_length.done`
- Representative outputs: `results/finish/featuretypeCounts_length.done`
- Execution targets: `featuretypeCounts_length`
- Downstream handoff: `pred_ORF`

## Guardrails
- Treat `results/finish/featuretypeCounts_length.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/featuretypeCounts_length.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pred_ORF` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/featuretypeCounts_length.done` exists and `pred_ORF` can proceed without re-running featuretypeCounts length.
