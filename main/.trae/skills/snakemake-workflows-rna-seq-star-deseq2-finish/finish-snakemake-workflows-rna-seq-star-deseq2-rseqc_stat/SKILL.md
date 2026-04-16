---
name: finish-snakemake-workflows-rna-seq-star-deseq2-rseqc_stat
description: Use this skill when orchestrating the retained "rseqc_stat" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the rseqc stat stage tied to upstream `rseqc_junction_saturation` and the downstream handoff to `rseqc_infer`. It tracks completion via `results/finish/rseqc_stat.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: rseqc_stat
  step_name: rseqc stat
---

# Scope
Use this skill only for the `rseqc_stat` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `rseqc_junction_saturation`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/rseqc_stat.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_stat.done`
- Representative outputs: `results/finish/rseqc_stat.done`
- Execution targets: `rseqc_stat`
- Downstream handoff: `rseqc_infer`

## Guardrails
- Treat `results/finish/rseqc_stat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_stat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_infer` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_stat.done` exists and `rseqc_infer` can proceed without re-running rseqc stat.
