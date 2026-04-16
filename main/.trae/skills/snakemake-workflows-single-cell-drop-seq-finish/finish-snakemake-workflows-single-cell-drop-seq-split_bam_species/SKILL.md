---
name: finish-snakemake-workflows-single-cell-drop-seq-split_bam_species
description: Use this skill when orchestrating the retained "split_bam_species" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the split bam species stage tied to upstream `compress_mtx` and the downstream handoff to `extract_all_umi_expression`. It tracks completion via `results/finish/split_bam_species.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: split_bam_species
  step_name: split bam species
---

# Scope
Use this skill only for the `split_bam_species` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `compress_mtx`
- Step file: `finish/single-cell-drop-seq-finish/steps/split_bam_species.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/split_bam_species.done`
- Representative outputs: `results/finish/split_bam_species.done`
- Execution targets: `split_bam_species`
- Downstream handoff: `extract_all_umi_expression`

## Guardrails
- Treat `results/finish/split_bam_species.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/split_bam_species.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract_all_umi_expression` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/split_bam_species.done` exists and `extract_all_umi_expression` can proceed without re-running split bam species.
