---
name: finish-snakemake-workflows-single-cell-drop-seq-pigz_unmapped
description: Use this skill when orchestrating the retained "pigz_unmapped" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the pigz unmapped stage tied to upstream `multiqc_star` and the downstream handoff to `MergeBamAlignment`. It tracks completion via `results/finish/pigz_unmapped.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: pigz_unmapped
  step_name: pigz unmapped
---

# Scope
Use this skill only for the `pigz_unmapped` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `multiqc_star`
- Step file: `finish/single-cell-drop-seq-finish/steps/pigz_unmapped.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pigz_unmapped.done`
- Representative outputs: `results/finish/pigz_unmapped.done`
- Execution targets: `pigz_unmapped`
- Downstream handoff: `MergeBamAlignment`

## Guardrails
- Treat `results/finish/pigz_unmapped.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pigz_unmapped.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `MergeBamAlignment` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pigz_unmapped.done` exists and `MergeBamAlignment` can proceed without re-running pigz unmapped.
