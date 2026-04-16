---
name: finish-kallisto-sleuth-prepare-references
description: Use this skill when orchestrating the retained "prepare_references" step of the RNA-seq Kallisto Sleuth finish workflow. It captures the normalized-input dependency, the reference index outputs, and the handoff into read preparation.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: RNA-seq Kallisto Sleuth Finish Workflow
  step_id: prepare_references
  step_name: Prepare kallisto references
---

# Scope
Use this skill only for the `prepare_references` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `normalize_inputs`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/prepare_references.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_references.done`
- Representative outputs: `resources/transcriptome.cdna.fasta`, `resources/genome.gtf`, `resources/transcripts_annotation.results.rds`, `resources/transcripts_annotation.results.tsv`, `resources/transcripts_annotation.main_transcript_strand_length.tsv`
- Execution targets: `resources/transcriptome.cdna.fasta`, `resources/genome.gtf`, `resources/transcripts_annotation.results.rds`, `resources/transcripts_annotation.results.tsv`, `resources/transcripts_annotation.main_transcript_strand_length.tsv`
- Downstream handoff: `prepare_reads`

## Guardrails
- Treat `results/finish/prepare_references.done` as the authoritative completion signal for the wrapped finish step.
- Reuse the shared reference artifact cache when available; do not refetch BioMart-derived transcript annotations if the cached bundle already matches the config.
- Keep the step atomic: build only the explicit reference targets listed above, not a larger `all --until ...` slice of the source workflow.

## Done Criteria
Mark this step complete only when the kallisto reference assets exist and the read-preparation stage can use them without rebuilding reference inputs.
