---
name: finish-mckellardw-slide-snake-ont_1c_fastq_call_bc_from_adapter
description: Use this skill when orchestrating the retained "ont_1c_fastq_call_bc_from_adapter" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1c fastq call bc from adapter stage tied to upstream `ont_1b_cutadapt_summary` and the downstream handoff to `ont_1c_filter_barcodes`. It tracks completion via `results/finish/ont_1c_fastq_call_bc_from_adapter.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1c_fastq_call_bc_from_adapter
  step_name: ont 1c fastq call bc from adapter
---

# Scope
Use this skill only for the `ont_1c_fastq_call_bc_from_adapter` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1b_cutadapt_summary`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1c_fastq_call_bc_from_adapter.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1c_fastq_call_bc_from_adapter.done`
- Representative outputs: `results/finish/ont_1c_fastq_call_bc_from_adapter.done`
- Execution targets: `ont_1c_fastq_call_bc_from_adapter`
- Downstream handoff: `ont_1c_filter_barcodes`

## Guardrails
- Treat `results/finish/ont_1c_fastq_call_bc_from_adapter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1c_fastq_call_bc_from_adapter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1c_filter_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1c_fastq_call_bc_from_adapter.done` exists and `ont_1c_filter_barcodes` can proceed without re-running ont 1c fastq call bc from adapter.
