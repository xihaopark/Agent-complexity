---
name: finish-tgirke-systempiperdata-chipseq-bowtie2_index
description: Use this skill when orchestrating the retained "bowtie2_index" step of the tgirke systempiperdata chipseq finish finish workflow. It keeps the bowtie2 index stage tied to upstream `custom_preprocessing_function` and the downstream handoff to `bowtie2_alignment`. It tracks completion via `results/finish/bowtie2_index.done`.
metadata:
  workflow_id: tgirke-systempiperdata-chipseq-finish
  workflow_name: tgirke systempiperdata chipseq finish
  step_id: bowtie2_index
  step_name: bowtie2 index
---

# Scope
Use this skill only for the `bowtie2_index` step in `tgirke-systempiperdata-chipseq-finish`.

## Orchestration
- Upstream requirements: `custom_preprocessing_function`
- Step file: `finish/tgirke-systempiperdata-chipseq-finish/steps/bowtie2_index.smk`
- Config file: `finish/tgirke-systempiperdata-chipseq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bowtie2_index.done`
- Representative outputs: `results/finish/bowtie2_index.done`
- Execution targets: `bowtie2_index`
- Downstream handoff: `bowtie2_alignment`

## Guardrails
- Treat `results/finish/bowtie2_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bowtie2_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bowtie2_alignment` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bowtie2_index.done` exists and `bowtie2_alignment` can proceed without re-running bowtie2 index.
