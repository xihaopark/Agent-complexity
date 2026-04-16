---
name: finish-snakemake-workflows-single-cell-drop-seq-multiqc_star
description: Use this skill when orchestrating the retained "multiqc_star" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the multiqc star stage tied to upstream `STAR_align` and the downstream handoff to `pigz_unmapped`. It tracks completion via `results/finish/multiqc_star.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: multiqc_star
  step_name: multiqc star
---

# Scope
Use this skill only for the `multiqc_star` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `STAR_align`
- Step file: `finish/single-cell-drop-seq-finish/steps/multiqc_star.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/multiqc_star.done`
- Representative outputs: `results/finish/multiqc_star.done`
- Execution targets: `multiqc_star`
- Downstream handoff: `pigz_unmapped`

## Guardrails
- Treat `results/finish/multiqc_star.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/multiqc_star.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pigz_unmapped` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/multiqc_star.done` exists and `pigz_unmapped` can proceed without re-running multiqc star.
