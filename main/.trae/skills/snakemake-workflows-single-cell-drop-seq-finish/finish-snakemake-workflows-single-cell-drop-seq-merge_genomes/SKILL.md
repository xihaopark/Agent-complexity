---
name: finish-snakemake-workflows-single-cell-drop-seq-merge_genomes
description: Use this skill when orchestrating the retained "merge_genomes" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the merge genomes stage tied to upstream `rename_genome` and the downstream handoff to `merge_annotations`. It tracks completion via `results/finish/merge_genomes.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: merge_genomes
  step_name: merge genomes
---

# Scope
Use this skill only for the `merge_genomes` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `rename_genome`
- Step file: `finish/single-cell-drop-seq-finish/steps/merge_genomes.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_genomes.done`
- Representative outputs: `results/finish/merge_genomes.done`
- Execution targets: `merge_genomes`
- Downstream handoff: `merge_annotations`

## Guardrails
- Treat `results/finish/merge_genomes.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_genomes.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_annotations` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_genomes.done` exists and `merge_annotations` can proceed without re-running merge genomes.
