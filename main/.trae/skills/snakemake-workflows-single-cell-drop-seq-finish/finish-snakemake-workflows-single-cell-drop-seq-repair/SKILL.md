---
name: finish-snakemake-workflows-single-cell-drop-seq-repair
description: Use this skill when orchestrating the retained "repair" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the repair stage tied to upstream `clean_cutadapt` and the downstream handoff to `detect_barcodes`. It tracks completion via `results/finish/repair.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: repair
  step_name: repair
---

# Scope
Use this skill only for the `repair` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `clean_cutadapt`
- Step file: `finish/single-cell-drop-seq-finish/steps/repair.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/repair.done`
- Representative outputs: `results/finish/repair.done`
- Execution targets: `repair`
- Downstream handoff: `detect_barcodes`

## Guardrails
- Treat `results/finish/repair.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/repair.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `detect_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/repair.done` exists and `detect_barcodes` can proceed without re-running repair.
