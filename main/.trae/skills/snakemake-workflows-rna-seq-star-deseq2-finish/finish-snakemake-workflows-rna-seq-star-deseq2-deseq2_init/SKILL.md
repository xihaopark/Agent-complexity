---
name: finish-snakemake-workflows-rna-seq-star-deseq2-deseq2_init
description: Use this skill when orchestrating the retained "deseq2_init" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the deseq2 init stage tied to upstream `gene_2_symbol` and the downstream handoff to `pca`. It tracks completion via `results/finish/deseq2_init.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: deseq2_init
  step_name: deseq2 init
---

# Scope
Use this skill only for the `deseq2_init` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `gene_2_symbol`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/deseq2_init.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/deseq2_init.done`
- Representative outputs: `results/finish/deseq2_init.done`
- Execution targets: `deseq2_init`
- Downstream handoff: `pca`

## Guardrails
- Treat `results/finish/deseq2_init.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/deseq2_init.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pca` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/deseq2_init.done` exists and `pca` can proceed without re-running deseq2 init.
