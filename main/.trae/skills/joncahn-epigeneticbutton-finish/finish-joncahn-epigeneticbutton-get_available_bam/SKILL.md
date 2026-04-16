---
name: finish-joncahn-epigeneticbutton-get_available_bam
description: Use this skill when orchestrating the retained "get_available_bam" step of the joncahn epigeneticbutton finish finish workflow. It keeps the get available bam stage tied to upstream `process_fastq_se` and the downstream handoff to `make_bt2_indices`. It tracks completion via `results/finish/get_available_bam.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: get_available_bam
  step_name: get available bam
---

# Scope
Use this skill only for the `get_available_bam` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `process_fastq_se`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/get_available_bam.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_available_bam.done`
- Representative outputs: `results/finish/get_available_bam.done`
- Execution targets: `get_available_bam`
- Downstream handoff: `make_bt2_indices`

## Guardrails
- Treat `results/finish/get_available_bam.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_available_bam.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_bt2_indices` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_available_bam.done` exists and `make_bt2_indices` can proceed without re-running get available bam.
