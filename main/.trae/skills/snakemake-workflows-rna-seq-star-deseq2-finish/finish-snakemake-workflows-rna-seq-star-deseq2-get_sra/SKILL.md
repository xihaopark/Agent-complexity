---
name: finish-snakemake-workflows-rna-seq-star-deseq2-get_sra
description: Use this skill when orchestrating the retained "get_sra" step of the snakemake workflows rna seq star deseq2 finish finish workflow. It keeps the get sra stage tied to upstream `star_index` and the downstream handoff to `fastp_se`. It tracks completion via `results/finish/get_sra.done`.
metadata:
  workflow_id: rna-seq-star-deseq2-finish
  workflow_name: snakemake workflows rna seq star deseq2 finish
  step_id: get_sra
  step_name: get sra
---

# Scope
Use this skill only for the `get_sra` step in `rna-seq-star-deseq2-finish`.

## Orchestration
- Upstream requirements: `star_index`
- Step file: `finish/rna-seq-star-deseq2-finish/steps/get_sra.smk`
- Config file: `finish/rna-seq-star-deseq2-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_sra.done`
- Representative outputs: `results/finish/get_sra.done`
- Execution targets: `get_sra`
- Downstream handoff: `fastp_se`

## Guardrails
- Treat `results/finish/get_sra.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_sra.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `fastp_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_sra.done` exists and `fastp_se` can proceed without re-running get sra.
