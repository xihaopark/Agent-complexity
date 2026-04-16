---
name: finish-tgirke-systempiperdata-riboseq-run_edger
description: Use this skill when orchestrating the retained "run_edgeR" step of the tgirke systempiperdata riboseq finish finish workflow. It keeps the run edgeR stage tied to upstream `sample_tree` and the downstream handoff to `custom_annot`. It tracks completion via `results/finish/run_edgeR.done`.
metadata:
  workflow_id: tgirke-systempiperdata-riboseq-finish
  workflow_name: tgirke systempiperdata riboseq finish
  step_id: run_edgeR
  step_name: run edgeR
---

# Scope
Use this skill only for the `run_edgeR` step in `tgirke-systempiperdata-riboseq-finish`.

## Orchestration
- Upstream requirements: `sample_tree`
- Step file: `finish/tgirke-systempiperdata-riboseq-finish/steps/run_edgeR.smk`
- Config file: `finish/tgirke-systempiperdata-riboseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/run_edgeR.done`
- Representative outputs: `results/finish/run_edgeR.done`
- Execution targets: `run_edgeR`
- Downstream handoff: `custom_annot`

## Guardrails
- Treat `results/finish/run_edgeR.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/run_edgeR.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `custom_annot` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/run_edgeR.done` exists and `custom_annot` can proceed without re-running run edgeR.
