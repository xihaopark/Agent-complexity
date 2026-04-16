---
name: finish-mckellardw-slide-snake-ont_1b_r1_hardtrimming
description: Use this skill when orchestrating the retained "ont_1b_R1_hardTrimming" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1b R1 hardTrimming stage tied to upstream `ont_1b_cutadapt` and the downstream handoff to `ont_1b_R1_internalTrim`. It tracks completion via `results/finish/ont_1b_R1_hardTrimming.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1b_R1_hardTrimming
  step_name: ont 1b R1 hardTrimming
---

# Scope
Use this skill only for the `ont_1b_R1_hardTrimming` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1b_cutadapt`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1b_R1_hardTrimming.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1b_R1_hardTrimming.done`
- Representative outputs: `results/finish/ont_1b_R1_hardTrimming.done`
- Execution targets: `ont_1b_R1_hardTrimming`
- Downstream handoff: `ont_1b_R1_internalTrim`

## Guardrails
- Treat `results/finish/ont_1b_R1_hardTrimming.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1b_R1_hardTrimming.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1b_R1_internalTrim` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1b_R1_hardTrimming.done` exists and `ont_1b_R1_internalTrim` can proceed without re-running ont 1b R1 hardTrimming.
