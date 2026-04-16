---
name: finish-mckellardw-slide-snake-ont_1b_r1_internaltrim
description: Use this skill when orchestrating the retained "ont_1b_R1_internalTrim" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1b R1 internalTrim stage tied to upstream `ont_1b_R1_hardTrimming` and the downstream handoff to `ont_1b_cutadapt_internalTrimming`. It tracks completion via `results/finish/ont_1b_R1_internalTrim.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1b_R1_internalTrim
  step_name: ont 1b R1 internalTrim
---

# Scope
Use this skill only for the `ont_1b_R1_internalTrim` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1b_R1_hardTrimming`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1b_R1_internalTrim.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1b_R1_internalTrim.done`
- Representative outputs: `results/finish/ont_1b_R1_internalTrim.done`
- Execution targets: `ont_1b_R1_internalTrim`
- Downstream handoff: `ont_1b_cutadapt_internalTrimming`

## Guardrails
- Treat `results/finish/ont_1b_R1_internalTrim.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1b_R1_internalTrim.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1b_cutadapt_internalTrimming` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1b_R1_internalTrim.done` exists and `ont_1b_cutadapt_internalTrimming` can proceed without re-running ont 1b R1 internalTrim.
