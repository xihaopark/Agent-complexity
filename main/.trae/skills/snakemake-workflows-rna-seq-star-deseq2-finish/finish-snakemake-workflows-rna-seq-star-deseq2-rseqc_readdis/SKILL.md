---
name: finish-snakemake-workflows-rna-seq-star-deseq2-rseqc_readdis
description: Use this skill when orchestrating the retained "rseqc_readdis" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the rseqc readdis stage tied to upstream `rseqc_innerdis` and the downstream handoff to `rseqc_readdup`. It tracks completion via `results/finish/rseqc_readdis.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: rseqc_readdis
  step_name: rseqc readdis
---

# Scope
Use this skill only for the `rseqc_readdis` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `rseqc_innerdis`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/rseqc_readdis.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/rseqc_readdis.done`
- Representative outputs: `results/finish/rseqc_readdis.done`
- Execution targets: `rseqc_readdis`
- Downstream handoff: `rseqc_readdup`

## Guardrails
- Treat `results/finish/rseqc_readdis.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/rseqc_readdis.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `rseqc_readdup` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/rseqc_readdis.done` exists and `rseqc_readdup` can proceed without re-running rseqc readdis.
