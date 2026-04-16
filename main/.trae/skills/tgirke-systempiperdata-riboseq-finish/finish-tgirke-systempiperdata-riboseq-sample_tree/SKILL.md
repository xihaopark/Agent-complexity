---
name: finish-tgirke-systempiperdata-riboseq-sample_tree
description: Use this skill when orchestrating the retained "sample_tree" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the sample tree stage tied to upstream `read_counting` and the downstream handoff to `run_edgeR`. It tracks completion via `results/finish/sample_tree.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: sample_tree
  step_name: sample tree
---

# Scope
Use this skill only for the `sample_tree` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `read_counting`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/sample_tree.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sample_tree.done`
- Representative outputs: `results/finish/sample_tree.done`
- Execution targets: `sample_tree`
- Downstream handoff: `run_edgeR`

## Guardrails
- Treat `results/finish/sample_tree.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sample_tree.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `run_edgeR` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sample_tree.done` exists and `run_edgeR` can proceed without re-running sample tree.
