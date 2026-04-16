---
name: finish-joncahn-epigeneticbutton-dispatch_srna_fastq
description: Use this skill when orchestrating the retained "dispatch_srna_fastq" step of the joncahn epigeneticbutton finish finish workflow. It keeps the dispatch srna fastq stage tied to upstream `filter_structural_rna` and the downstream handoff to `make_bowtie1_indices`. It tracks completion via `results/finish/dispatch_srna_fastq.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: dispatch_srna_fastq
  step_name: dispatch srna fastq
---

# Scope
Use this skill only for the `dispatch_srna_fastq` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `filter_structural_rna`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/dispatch_srna_fastq.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/dispatch_srna_fastq.done`
- Representative outputs: `results/finish/dispatch_srna_fastq.done`
- Execution targets: `dispatch_srna_fastq`
- Downstream handoff: `make_bowtie1_indices`

## Guardrails
- Treat `results/finish/dispatch_srna_fastq.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/dispatch_srna_fastq.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_bowtie1_indices` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/dispatch_srna_fastq.done` exists and `make_bowtie1_indices` can proceed without re-running dispatch srna fastq.
