---
name: finish-tgirke-systempiperdata-chipseq-parse_peak_sequences
description: Use this skill when orchestrating the retained "parse_peak_sequences" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the parse peak sequences stage tied to upstream `go_enrich` and the downstream handoff to `bcrank_enrich`. It tracks completion via `results/finish/parse_peak_sequences.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: parse_peak_sequences
  step_name: parse peak sequences
---

# Scope
Use this skill only for the `parse_peak_sequences` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `go_enrich`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/parse_peak_sequences.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/parse_peak_sequences.done`
- Representative outputs: `results/finish/parse_peak_sequences.done`
- Execution targets: `parse_peak_sequences`
- Downstream handoff: `bcrank_enrich`

## Guardrails
- Treat `results/finish/parse_peak_sequences.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/parse_peak_sequences.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bcrank_enrich` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/parse_peak_sequences.done` exists and `bcrank_enrich` can proceed without re-running parse peak sequences.
