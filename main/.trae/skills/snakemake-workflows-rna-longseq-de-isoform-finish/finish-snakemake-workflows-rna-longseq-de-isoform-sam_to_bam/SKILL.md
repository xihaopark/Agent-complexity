---
name: finish-snakemake-workflows-rna-longseq-de-isoform-sam_to_bam
description: Use this skill when orchestrating the retained "sam_to_bam" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the sam to bam stage tied to upstream `map_reads` and the downstream handoff to `bam_sort`. It tracks completion via `results/finish/sam_to_bam.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: sam_to_bam
  step_name: sam to bam
---

# Scope
Use this skill only for the `sam_to_bam` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `map_reads`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/sam_to_bam.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sam_to_bam.done`
- Representative outputs: `results/finish/sam_to_bam.done`
- Execution targets: `sam_to_bam`
- Downstream handoff: `bam_sort`

## Guardrails
- Treat `results/finish/sam_to_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sam_to_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam_sort` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sam_to_bam.done` exists and `bam_sort` can proceed without re-running sam to bam.
