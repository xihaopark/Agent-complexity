---
name: finish-snakemake-workflows-single-cell-drop-seq-tagreadwithgeneexon
description: Use this skill when orchestrating the retained "TagReadWithGeneExon" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the TagReadWithGeneExon stage tied to upstream `MergeBamAlignment` and the downstream handoff to `DetectBeadSubstitutionErrors`. It tracks completion via `results/finish/TagReadWithGeneExon.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: TagReadWithGeneExon
  step_name: TagReadWithGeneExon
---

# Scope
Use this skill only for the `TagReadWithGeneExon` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `MergeBamAlignment`
- Step file: `finish/single-cell-drop-seq-finish/steps/TagReadWithGeneExon.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/TagReadWithGeneExon.done`
- Representative outputs: `results/finish/TagReadWithGeneExon.done`
- Execution targets: `TagReadWithGeneExon`
- Downstream handoff: `DetectBeadSubstitutionErrors`

## Guardrails
- Treat `results/finish/TagReadWithGeneExon.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/TagReadWithGeneExon.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `DetectBeadSubstitutionErrors` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/TagReadWithGeneExon.done` exists and `DetectBeadSubstitutionErrors` can proceed without re-running TagReadWithGeneExon.
