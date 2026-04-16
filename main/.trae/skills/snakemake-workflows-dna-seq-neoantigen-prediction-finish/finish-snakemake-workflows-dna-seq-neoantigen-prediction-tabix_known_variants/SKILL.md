---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-tabix_known_variants
description: Use this skill when orchestrating the retained "tabix_known_variants" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the tabix known variants stage tied to upstream `bam_index` and the downstream handoff to `gzip_fastq`. It tracks completion via `results/finish/tabix_known_variants.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: tabix_known_variants
  step_name: tabix known variants
---

# Scope
Use this skill only for the `tabix_known_variants` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `bam_index`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/tabix_known_variants.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/tabix_known_variants.done`
- Representative outputs: `results/finish/tabix_known_variants.done`
- Execution targets: `tabix_known_variants`
- Downstream handoff: `gzip_fastq`

## Guardrails
- Treat `results/finish/tabix_known_variants.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/tabix_known_variants.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gzip_fastq` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/tabix_known_variants.done` exists and `gzip_fastq` can proceed without re-running tabix known variants.
