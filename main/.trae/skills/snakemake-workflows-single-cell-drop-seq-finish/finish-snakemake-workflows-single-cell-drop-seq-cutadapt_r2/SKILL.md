---
name: finish-snakemake-workflows-single-cell-drop-seq-cutadapt_r2
description: Use this skill when orchestrating the retained "cutadapt_R2" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the cutadapt R2 stage tied to upstream `cutadapt_R1` and the downstream handoff to `clean_cutadapt`. It tracks completion via `results/finish/cutadapt_R2.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: cutadapt_R2
  step_name: cutadapt R2
---

# Scope
Use this skill only for the `cutadapt_R2` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `cutadapt_R1`
- Step file: `finish/single-cell-drop-seq-finish/steps/cutadapt_R2.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cutadapt_R2.done`
- Representative outputs: `results/finish/cutadapt_R2.done`
- Execution targets: `cutadapt_R2`
- Downstream handoff: `clean_cutadapt`

## Guardrails
- Treat `results/finish/cutadapt_R2.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cutadapt_R2.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `clean_cutadapt` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cutadapt_R2.done` exists and `clean_cutadapt` can proceed without re-running cutadapt R2.
