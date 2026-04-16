---
name: finish-snakemake-workflows-rna-seq-star-deseq2-deseq2
description: Use this skill when orchestrating the retained "deseq2" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the deseq2 stage tied to upstream `pca` and the downstream handoff to `all`. It tracks completion via `results/finish/deseq2.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: deseq2
  step_name: deseq2
---

# Scope
Use this skill only for the `deseq2` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `pca`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/deseq2.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/deseq2.done`
- Representative outputs: `results/finish/deseq2.done`
- Execution targets: `deseq2`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/deseq2.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/deseq2.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/deseq2.done` exists and `all` can proceed without re-running deseq2.
