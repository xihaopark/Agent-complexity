---
name: finish-dwheelerau-snakemake-rnaseq-counts-sam_to_bam
description: Use this skill when orchestrating the retained "sam_to_bam" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the sam to bam stage tied to upstream `aln` and the downstream handoff to `do_counts`. It tracks completion via `results/finish/sam_to_bam.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: sam_to_bam
  step_name: sam to bam
---

# Scope
Use this skill only for the `sam_to_bam` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: `aln`
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/sam_to_bam.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/sam_to_bam.done`
- Representative outputs: `results/finish/sam_to_bam.done`
- Execution targets: `sam_to_bam`
- Downstream handoff: `do_counts`

## Guardrails
- Treat `results/finish/sam_to_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/sam_to_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `do_counts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/sam_to_bam.done` exists and `do_counts` can proceed without re-running sam to bam.
