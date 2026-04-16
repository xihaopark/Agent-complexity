---
name: finish-tgirke-systempiperdata-rnaseq-sample_tree
description: Use this skill when orchestrating the retained "sample_tree" step of the tgirke systempiperdata rnaseq finish finish workflow. It keeps the sample tree stage tied to upstream `read_counting` and the downstream handoff to `run_edger`. It tracks completion via `results/finish/sample_tree.done`.
metadata:
  workflow_id: tgirke-systempiperdata-rnaseq-finish
  workflow_name: tgirke systempiperdata rnaseq finish
  step_id: sample_tree
  step_name: sample tree
---

# Scope
Use this skill only for the `sample_tree` step in `tgirke-systempiperdata-rnaseq-finish`.

## Orchestration
- Upstream requirements: `read_counting`
- Step file: `finish/tgirke-systempiperdata-rnaseq-finish/steps/sample_tree.smk`
- Config file: `finish/tgirke-systempiperdata-rnaseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sample_tree.done`
- Representative outputs: `results/finish/sample_tree.done`
- Execution targets: `sample_tree`
- Downstream handoff: `run_edger`

## Guardrails
- Treat `results/finish/sample_tree.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sample_tree.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `run_edger` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sample_tree.done` exists and `run_edger` can proceed without re-running sample tree.
