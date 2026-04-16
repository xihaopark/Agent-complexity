---
name: finish-varlociraptor-prepare-reads
description: Use this skill when orchestrating the retained "prepare_reads" step of the DNA-seq Varlociraptor finish workflow. It bridges the prepared reference bundle to FASTQ or BAM staging so mapping can start with normalized inputs.
metadata:
  workflow_id: dna-seq-varlociraptor-finish
  workflow_name: DNA-seq Varlociraptor Finish Workflow
  step_id: prepare_reads
  step_name: Prepare FASTQ or BAM inputs
---

# Scope
Use this skill only for the `prepare_reads` step in `dna-seq-varlociraptor-finish`.

## Orchestration
- Upstream requirements: `prepare_references`
- Step file: `finish/dna-seq-varlociraptor-finish/steps/prepare_reads.smk`
- Config file: `finish/dna-seq-varlociraptor-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_reads.done`
- Representative outputs: `results/prepared_reads/*`
- Downstream handoff: `mapping`

## Guardrails
- Treat `results/finish/prepare_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage scoped to staged FASTQ or BAM assets needed by mapping.

## Done Criteria
Mark this step complete only when FASTQ or BAM inputs are staged for all planned samples and the mapping step can consume them directly.
