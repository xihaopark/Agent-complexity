---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-gzip_fastq
description: Use this skill when orchestrating the retained "gzip_fastq" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the gzip fastq stage tied to upstream `tabix_known_variants` and the downstream handoff to `tsv_to_excel`. It tracks completion via `results/finish/gzip_fastq.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: gzip_fastq
  step_name: gzip fastq
---

# Scope
Use this skill only for the `gzip_fastq` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `tabix_known_variants`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/gzip_fastq.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gzip_fastq.done`
- Representative outputs: `results/finish/gzip_fastq.done`
- Execution targets: `gzip_fastq`
- Downstream handoff: `tsv_to_excel`

## Guardrails
- Treat `results/finish/gzip_fastq.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gzip_fastq.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `tsv_to_excel` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gzip_fastq.done` exists and `tsv_to_excel` can proceed without re-running gzip fastq.
