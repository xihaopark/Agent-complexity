---
name: finish-snakemake-workflows-rna-seq-star-deseq2-star_index
description: Use this skill when orchestrating the retained "star_index" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the star index stage tied to upstream `bwa_index` and the downstream handoff to `get_sra`. It tracks completion via `results/finish/star_index.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: star_index
  step_name: star index
---

# Scope
Use this skill only for the `star_index` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `bwa_index`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/star_index.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/star_index.done`
- Representative outputs: `results/finish/star_index.done`
- Execution targets: `star_index`
- Downstream handoff: `get_sra`

## Guardrails
- Treat `results/finish/star_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/star_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_sra` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/star_index.done` exists and `get_sra` can proceed without re-running star index.
