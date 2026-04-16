---
name: finish-snakemake-workflows-rna-seq-star-deseq2-pca
description: Use this skill when orchestrating the retained "pca" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the pca stage tied to upstream `deseq2_init` and the downstream handoff to `deseq2`. It tracks completion via `results/finish/pca.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: pca
  step_name: pca
---

# Scope
Use this skill only for the `pca` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `deseq2_init`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/pca.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pca.done`
- Representative outputs: `results/finish/pca.done`
- Execution targets: `pca`
- Downstream handoff: `deseq2`

## Guardrails
- Treat `results/finish/pca.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pca.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `deseq2` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pca.done` exists and `deseq2` can proceed without re-running pca.
