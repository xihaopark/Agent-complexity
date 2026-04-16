---
name: finish-snakemake-workflows-single-cell-drop-seq-clean_cutadapt
description: Use this skill when orchestrating the retained "clean_cutadapt" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the clean cutadapt stage tied to upstream `cutadapt_R2` and the downstream handoff to `repair`. It tracks completion via `results/finish/clean_cutadapt.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: clean_cutadapt
  step_name: clean cutadapt
---

# Scope
Use this skill only for the `clean_cutadapt` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `cutadapt_R2`
- Step file: `finish/single-cell-drop-seq-finish/steps/clean_cutadapt.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/clean_cutadapt.done`
- Representative outputs: `results/finish/clean_cutadapt.done`
- Execution targets: `clean_cutadapt`
- Downstream handoff: `repair`

## Guardrails
- Treat `results/finish/clean_cutadapt.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/clean_cutadapt.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `repair` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/clean_cutadapt.done` exists and `repair` can proceed without re-running clean cutadapt.
