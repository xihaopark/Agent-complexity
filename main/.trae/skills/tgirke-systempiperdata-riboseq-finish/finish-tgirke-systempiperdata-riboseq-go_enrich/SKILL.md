---
name: finish-tgirke-systempiperdata-riboseq-go_enrich
description: Use this skill when orchestrating the retained "go_enrich" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the go enrich stage tied to upstream `get_go_annot` and the downstream handoff to `go_plot`. It tracks completion via `results/finish/go_enrich.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: go_enrich
  step_name: go enrich
---

# Scope
Use this skill only for the `go_enrich` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `get_go_annot`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/go_enrich.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/go_enrich.done`
- Representative outputs: `results/finish/go_enrich.done`
- Execution targets: `go_enrich`
- Downstream handoff: `go_plot`

## Guardrails
- Treat `results/finish/go_enrich.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/go_enrich.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `go_plot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/go_enrich.done` exists and `go_plot` can proceed without re-running go enrich.
