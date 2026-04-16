---
name: finish-snakemake-workflows-single-cell-drop-seq-rename_genome
description: Use this skill when orchestrating the retained "rename_genome" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the rename genome stage tied to upstream `download_genome` and the downstream handoff to `merge_genomes`. It tracks completion via `results/finish/rename_genome.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: rename_genome
  step_name: rename genome
---

# Scope
Use this skill only for the `rename_genome` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `download_genome`
- Step file: `finish/single-cell-drop-seq-finish/steps/rename_genome.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rename_genome.done`
- Representative outputs: `results/finish/rename_genome.done`
- Execution targets: `rename_genome`
- Downstream handoff: `merge_genomes`

## Guardrails
- Treat `results/finish/rename_genome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rename_genome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_genomes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rename_genome.done` exists and `merge_genomes` can proceed without re-running rename genome.
