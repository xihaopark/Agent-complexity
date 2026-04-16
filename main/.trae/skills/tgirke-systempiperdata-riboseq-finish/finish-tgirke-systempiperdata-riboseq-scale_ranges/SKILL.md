---
name: finish-tgirke-systempiperdata-riboseq-scale_ranges
description: Use this skill when orchestrating the retained "scale_ranges" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the scale ranges stage tied to upstream `pred_ORF` and the downstream handoff to `translate`. It tracks completion via `results/finish/scale_ranges.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: scale_ranges
  step_name: scale ranges
---

# Scope
Use this skill only for the `scale_ranges` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `pred_ORF`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/scale_ranges.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/scale_ranges.done`
- Representative outputs: `results/finish/scale_ranges.done`
- Execution targets: `scale_ranges`
- Downstream handoff: `translate`

## Guardrails
- Treat `results/finish/scale_ranges.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/scale_ranges.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `translate` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/scale_ranges.done` exists and `translate` can proceed without re-running scale ranges.
