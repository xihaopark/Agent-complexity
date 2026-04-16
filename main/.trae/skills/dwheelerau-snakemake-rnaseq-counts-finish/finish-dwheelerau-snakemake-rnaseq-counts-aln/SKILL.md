---
name: finish-dwheelerau-snakemake-rnaseq-counts-aln
description: Use this skill when orchestrating the retained "aln" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the aln stage tied to upstream `qc_trim` and the downstream handoff to `sam_to_bam`. It tracks completion via `results/finish/aln.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: aln
  step_name: aln
---

# Scope
Use this skill only for the `aln` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: `qc_trim`
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/aln.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/aln.done`
- Representative outputs: `results/finish/aln.done`
- Execution targets: `aln`
- Downstream handoff: `sam_to_bam`

## Guardrails
- Treat `results/finish/aln.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/aln.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `sam_to_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/aln.done` exists and `sam_to_bam` can proceed without re-running aln.
