---
name: finish-snakemake-workflows-rna-longseq-de-isoform-gff_to_gtf
description: Use this skill when orchestrating the retained "gff_to_gtf" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the gff to gtf stage tied to upstream `reads_manifest` and the downstream handoff to `bam_to_bed`. It tracks completion via `results/finish/gff_to_gtf.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: gff_to_gtf
  step_name: gff to gtf
---

# Scope
Use this skill only for the `gff_to_gtf` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `reads_manifest`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/gff_to_gtf.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gff_to_gtf.done`
- Representative outputs: `results/finish/gff_to_gtf.done`
- Execution targets: `gff_to_gtf`
- Downstream handoff: `bam_to_bed`

## Guardrails
- Treat `results/finish/gff_to_gtf.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gff_to_gtf.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam_to_bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gff_to_gtf.done` exists and `bam_to_bed` can proceed without re-running gff to gtf.
