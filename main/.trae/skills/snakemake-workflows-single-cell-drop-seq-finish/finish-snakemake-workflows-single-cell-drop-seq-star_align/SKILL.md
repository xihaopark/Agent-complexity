---
name: finish-snakemake-workflows-single-cell-drop-seq-star_align
description: Use this skill when orchestrating the retained "STAR_align" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the STAR align stage tied to upstream `repair_barcodes` and the downstream handoff to `multiqc_star`. It tracks completion via `results/finish/STAR_align.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: STAR_align
  step_name: STAR align
---

# Scope
Use this skill only for the `STAR_align` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `repair_barcodes`
- Step file: `finish/single-cell-drop-seq-finish/steps/STAR_align.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/STAR_align.done`
- Representative outputs: `results/finish/STAR_align.done`
- Execution targets: `STAR_align`
- Downstream handoff: `multiqc_star`

## Guardrails
- Treat `results/finish/STAR_align.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/STAR_align.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `multiqc_star` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/STAR_align.done` exists and `multiqc_star` can proceed without re-running STAR align.
