---
name: finish-tgirke-systempiperdata-chipseq-diff_bind_analysis
description: Use this skill when orchestrating the retained "diff_bind_analysis" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the diff bind analysis stage tied to upstream `count_peak_ranges` and the downstream handoff to `go_enrich`. It tracks completion via `results/finish/diff_bind_analysis.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: diff_bind_analysis
  step_name: diff bind analysis
---

# Scope
Use this skill only for the `diff_bind_analysis` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `count_peak_ranges`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/diff_bind_analysis.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/diff_bind_analysis.done`
- Representative outputs: `results/finish/diff_bind_analysis.done`
- Execution targets: `diff_bind_analysis`
- Downstream handoff: `go_enrich`

## Guardrails
- Treat `results/finish/diff_bind_analysis.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/diff_bind_analysis.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `go_enrich` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/diff_bind_analysis.done` exists and `go_enrich` can proceed without re-running diff bind analysis.
