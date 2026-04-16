---
name: finish-snakemake-workflows-rna-longseq-de-isoform-bam_to_bed
description: Use this skill when orchestrating the retained "bam_to_bed" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the bam to bed stage tied to upstream `gff_to_gtf` and the downstream handoff to `concatenate_beds`. It tracks completion via `results/finish/bam_to_bed.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: bam_to_bed
  step_name: bam to bed
---

# Scope
Use this skill only for the `bam_to_bed` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `gff_to_gtf`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/bam_to_bed.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_to_bed.done`
- Representative outputs: `results/finish/bam_to_bed.done`
- Execution targets: `bam_to_bed`
- Downstream handoff: `concatenate_beds`

## Guardrails
- Treat `results/finish/bam_to_bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_to_bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `concatenate_beds` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_to_bed.done` exists and `concatenate_beds` can proceed without re-running bam to bed.
