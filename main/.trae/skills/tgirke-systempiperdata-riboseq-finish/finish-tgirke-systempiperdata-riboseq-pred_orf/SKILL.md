---
name: finish-tgirke-systempiperdata-riboseq-pred_orf
description: Use this skill when orchestrating the retained "pred_ORF" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the pred ORF stage tied to upstream `featuretypeCounts_length` and the downstream handoff to `scale_ranges`. It tracks completion via `results/finish/pred_ORF.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: pred_ORF
  step_name: pred ORF
---

# Scope
Use this skill only for the `pred_ORF` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `featuretypeCounts_length`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/pred_ORF.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pred_ORF.done`
- Representative outputs: `results/finish/pred_ORF.done`
- Execution targets: `pred_ORF`
- Downstream handoff: `scale_ranges`

## Guardrails
- Treat `results/finish/pred_ORF.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pred_ORF.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `scale_ranges` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pred_ORF.done` exists and `scale_ranges` can proceed without re-running pred ORF.
