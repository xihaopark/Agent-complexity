---
name: finish-joncahn-epigeneticbutton-make_bowtie1_indices
description: Use this skill when orchestrating the retained "make_bowtie1_indices" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make bowtie1 indices stage tied to upstream `dispatch_srna_fastq` and the downstream handoff to `make_bowtie1_indices_large`. It tracks completion via `results/finish/make_bowtie1_indices.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_bowtie1_indices
  step_name: make bowtie1 indices
---

# Scope
Use this skill only for the `make_bowtie1_indices` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `dispatch_srna_fastq`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_bowtie1_indices.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_bowtie1_indices.done`
- Representative outputs: `results/finish/make_bowtie1_indices.done`
- Execution targets: `make_bowtie1_indices`
- Downstream handoff: `make_bowtie1_indices_large`

## Guardrails
- Treat `results/finish/make_bowtie1_indices.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_bowtie1_indices.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_bowtie1_indices_large` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_bowtie1_indices.done` exists and `make_bowtie1_indices_large` can proceed without re-running make bowtie1 indices.
