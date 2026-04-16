---
name: finish-tgirke-systempiperdata-chipseq-go_enrich
description: Use this skill when orchestrating the retained "go_enrich" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the go enrich stage tied to upstream `diff_bind_analysis` and the downstream handoff to `parse_peak_sequences`. It tracks completion via `results/finish/go_enrich.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: go_enrich
  step_name: go enrich
---

# Scope
Use this skill only for the `go_enrich` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `diff_bind_analysis`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/go_enrich.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/go_enrich.done`
- Representative outputs: `results/finish/go_enrich.done`
- Execution targets: `go_enrich`
- Downstream handoff: `parse_peak_sequences`

## Guardrails
- Treat `results/finish/go_enrich.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/go_enrich.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `parse_peak_sequences` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/go_enrich.done` exists and `parse_peak_sequences` can proceed without re-running go enrich.
