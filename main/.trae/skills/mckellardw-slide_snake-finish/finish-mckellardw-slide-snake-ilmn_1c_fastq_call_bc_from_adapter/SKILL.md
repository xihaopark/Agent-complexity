---
name: finish-mckellardw-slide-snake-ilmn_1c_fastq_call_bc_from_adapter
description: Use this skill when orchestrating the retained "ilmn_1c_fastq_call_bc_from_adapter" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 1c fastq call bc from adapter stage tied to upstream `ilmn_1b_R1_internalTrimming` and the downstream handoff to `ilmn_1c_filter_barcodes`. It tracks completion via `results/finish/ilmn_1c_fastq_call_bc_from_adapter.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_1c_fastq_call_bc_from_adapter
  step_name: ilmn 1c fastq call bc from adapter
---

# Scope
Use this skill only for the `ilmn_1c_fastq_call_bc_from_adapter` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_1b_R1_internalTrimming`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_1c_fastq_call_bc_from_adapter.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_1c_fastq_call_bc_from_adapter.done`
- Representative outputs: `results/finish/ilmn_1c_fastq_call_bc_from_adapter.done`
- Execution targets: `ilmn_1c_fastq_call_bc_from_adapter`
- Downstream handoff: `ilmn_1c_filter_barcodes`

## Guardrails
- Treat `results/finish/ilmn_1c_fastq_call_bc_from_adapter.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_1c_fastq_call_bc_from_adapter.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_1c_filter_barcodes` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_1c_fastq_call_bc_from_adapter.done` exists and `ilmn_1c_filter_barcodes` can proceed without re-running ilmn 1c fastq call bc from adapter.
