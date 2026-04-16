---
name: finish-snakemake-workflows-rna-seq-star-deseq2-rseqc_infer
description: Use this skill when orchestrating the retained "rseqc_infer" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the rseqc infer stage tied to upstream `rseqc_stat` and the downstream handoff to `rseqc_innerdis`. It tracks completion via `results/finish/rseqc_infer.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: rseqc_infer
  step_name: rseqc infer
---

# Scope
Use this skill only for the `rseqc_infer` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `rseqc_stat`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/rseqc_infer.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_infer.done`
- Representative outputs: `results/finish/rseqc_infer.done`
- Execution targets: `rseqc_infer`
- Downstream handoff: `rseqc_innerdis`

## Guardrails
- Treat `results/finish/rseqc_infer.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_infer.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_innerdis` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_infer.done` exists and `rseqc_innerdis` can proceed without re-running rseqc infer.
