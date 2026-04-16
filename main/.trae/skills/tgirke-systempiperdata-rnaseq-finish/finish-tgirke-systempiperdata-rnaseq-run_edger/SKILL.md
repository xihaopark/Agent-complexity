---
name: finish-tgirke-systempiperdata-rnaseq-run_edger
description: Use this skill when orchestrating the retained "run_edger" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the run edger stage tied to upstream `sample_tree` and the downstream handoff to `custom_annot`. It tracks completion via `results/finish/run_edger.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: run_edger
  step_name: run edger
---

# Scope
Use this skill only for the `run_edger` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `sample_tree`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/run_edger.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/run_edger.done`
- Representative outputs: `results/finish/run_edger.done`
- Execution targets: `run_edger`
- Downstream handoff: `custom_annot`

## Guardrails
- Treat `results/finish/run_edger.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/run_edger.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `custom_annot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/run_edger.done` exists and `custom_annot` can proceed without re-running run edger.
