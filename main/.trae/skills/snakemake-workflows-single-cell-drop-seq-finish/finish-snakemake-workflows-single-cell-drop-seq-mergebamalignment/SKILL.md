---
name: finish-snakemake-workflows-single-cell-drop-seq-mergebamalignment
description: Use this skill when orchestrating the retained "MergeBamAlignment" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the MergeBamAlignment stage tied to upstream `pigz_unmapped` and the downstream handoff to `TagReadWithGeneExon`. It tracks completion via `results/finish/MergeBamAlignment.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: MergeBamAlignment
  step_name: MergeBamAlignment
---

# Scope
Use this skill only for the `MergeBamAlignment` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `pigz_unmapped`
- Step file: `finish/single-cell-drop-seq-finish/steps/MergeBamAlignment.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/MergeBamAlignment.done`
- Representative outputs: `results/finish/MergeBamAlignment.done`
- Execution targets: `MergeBamAlignment`
- Downstream handoff: `TagReadWithGeneExon`

## Guardrails
- Treat `results/finish/MergeBamAlignment.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/MergeBamAlignment.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `TagReadWithGeneExon` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/MergeBamAlignment.done` exists and `TagReadWithGeneExon` can proceed without re-running MergeBamAlignment.
