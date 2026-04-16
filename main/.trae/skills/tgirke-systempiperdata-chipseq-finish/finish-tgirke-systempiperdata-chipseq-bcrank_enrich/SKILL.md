---
name: finish-tgirke-systempiperdata-chipseq-bcrank_enrich
description: Use this skill when orchestrating the retained "bcrank_enrich" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the bcrank enrich stage tied to upstream `parse_peak_sequences` and the downstream handoff to `sessionInfo`. It tracks completion via `results/finish/bcrank_enrich.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: bcrank_enrich
  step_name: bcrank enrich
---

# Scope
Use this skill only for the `bcrank_enrich` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `parse_peak_sequences`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/bcrank_enrich.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bcrank_enrich.done`
- Representative outputs: `results/finish/bcrank_enrich.done`
- Execution targets: `bcrank_enrich`
- Downstream handoff: `sessionInfo`

## Guardrails
- Treat `results/finish/bcrank_enrich.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bcrank_enrich.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sessionInfo` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bcrank_enrich.done` exists and `sessionInfo` can proceed without re-running bcrank enrich.
