---
name: finish-snakemake-workflows-single-cell-drop-seq-compress_mtx
description: Use this skill when orchestrating the retained "compress_mtx" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the compress mtx stage tied to upstream `convert_long_to_mtx` and the downstream handoff to `split_bam_species`. It tracks completion via `results/finish/compress_mtx.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: compress_mtx
  step_name: compress mtx
---

# Scope
Use this skill only for the `compress_mtx` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `convert_long_to_mtx`
- Step file: `finish/single-cell-drop-seq-finish/steps/compress_mtx.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/compress_mtx.done`
- Representative outputs: `results/finish/compress_mtx.done`
- Execution targets: `compress_mtx`
- Downstream handoff: `split_bam_species`

## Guardrails
- Treat `results/finish/compress_mtx.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/compress_mtx.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `split_bam_species` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/compress_mtx.done` exists and `split_bam_species` can proceed without re-running compress mtx.
