---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-apply_bqsr
description: Use this skill when orchestrating the retained "apply_bqsr" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the apply bqsr stage tied to upstream `recalibrate_base_qualities` and the downstream handoff to `samtools_queryname_sort`. It tracks completion via `results/finish/apply_bqsr.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: apply_bqsr
  step_name: apply bqsr
---

# Scope
Use this skill only for the `apply_bqsr` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `recalibrate_base_qualities`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/apply_bqsr.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/apply_bqsr.done`
- Representative outputs: `results/finish/apply_bqsr.done`
- Execution targets: `apply_bqsr`
- Downstream handoff: `samtools_queryname_sort`

## Guardrails
- Treat `results/finish/apply_bqsr.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/apply_bqsr.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `samtools_queryname_sort` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/apply_bqsr.done` exists and `samtools_queryname_sort` can proceed without re-running apply bqsr.
