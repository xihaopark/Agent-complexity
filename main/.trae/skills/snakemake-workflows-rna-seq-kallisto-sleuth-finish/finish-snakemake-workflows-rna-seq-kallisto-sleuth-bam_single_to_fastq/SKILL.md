---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-bam_single_to_fastq
description: Use this skill when orchestrating the retained "bam_single_to_fastq" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the bam single to fastq stage tied to upstream `bam_paired_to_fastq` and the downstream handoff to `meta_compare_diffexp`. It tracks completion via `results/finish/bam_single_to_fastq.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: bam_single_to_fastq
  step_name: bam single to fastq
---

# Scope
Use this skill only for the `bam_single_to_fastq` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `bam_paired_to_fastq`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/bam_single_to_fastq.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_single_to_fastq.done`
- Representative outputs: `results/finish/bam_single_to_fastq.done`
- Execution targets: `bam_single_to_fastq`
- Downstream handoff: `meta_compare_diffexp`

## Guardrails
- Treat `results/finish/bam_single_to_fastq.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_single_to_fastq.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `meta_compare_diffexp` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_single_to_fastq.done` exists and `meta_compare_diffexp` can proceed without re-running bam single to fastq.
