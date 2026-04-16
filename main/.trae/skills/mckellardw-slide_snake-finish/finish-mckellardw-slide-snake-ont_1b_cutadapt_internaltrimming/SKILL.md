---
name: finish-mckellardw-slide-snake-ont_1b_cutadapt_internaltrimming
description: Use this skill when orchestrating the retained "ont_1b_cutadapt_internalTrimming" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1b cutadapt internalTrimming stage tied to upstream `ont_1b_R1_internalTrim` and the downstream handoff to `ont_1b_cutadapt_summary`. It tracks completion via `results/finish/ont_1b_cutadapt_internalTrimming.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1b_cutadapt_internalTrimming
  step_name: ont 1b cutadapt internalTrimming
---

# Scope
Use this skill only for the `ont_1b_cutadapt_internalTrimming` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1b_R1_internalTrim`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1b_cutadapt_internalTrimming.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1b_cutadapt_internalTrimming.done`
- Representative outputs: `results/finish/ont_1b_cutadapt_internalTrimming.done`
- Execution targets: `ont_1b_cutadapt_internalTrimming`
- Downstream handoff: `ont_1b_cutadapt_summary`

## Guardrails
- Treat `results/finish/ont_1b_cutadapt_internalTrimming.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1b_cutadapt_internalTrimming.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1b_cutadapt_summary` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1b_cutadapt_internalTrimming.done` exists and `ont_1b_cutadapt_summary` can proceed without re-running ont 1b cutadapt internalTrimming.
