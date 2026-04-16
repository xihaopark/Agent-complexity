---
name: finish-mckellardw-slide-snake-ilmn_1b_r1_internaltrimming
description: Use this skill when orchestrating the retained "ilmn_1b_R1_internalTrimming" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 1b R1 internalTrimming stage tied to upstream `ilmn_1b_R1_hardTrimming` and the downstream handoff to `ilmn_1c_fastq_call_bc_from_adapter`. It tracks completion via `results/finish/ilmn_1b_R1_internalTrimming.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_1b_R1_internalTrimming
  step_name: ilmn 1b R1 internalTrimming
---

# Scope
Use this skill only for the `ilmn_1b_R1_internalTrimming` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_1b_R1_hardTrimming`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_1b_R1_internalTrimming.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_1b_R1_internalTrimming.done`
- Representative outputs: `results/finish/ilmn_1b_R1_internalTrimming.done`
- Execution targets: `ilmn_1b_R1_internalTrimming`
- Downstream handoff: `ilmn_1c_fastq_call_bc_from_adapter`

## Guardrails
- Treat `results/finish/ilmn_1b_R1_internalTrimming.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_1b_R1_internalTrimming.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_1c_fastq_call_bc_from_adapter` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_1b_R1_internalTrimming.done` exists and `ilmn_1c_fastq_call_bc_from_adapter` can proceed without re-running ilmn 1b R1 internalTrimming.
