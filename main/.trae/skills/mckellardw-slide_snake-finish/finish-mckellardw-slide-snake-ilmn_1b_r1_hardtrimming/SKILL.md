---
name: finish-mckellardw-slide-snake-ilmn_1b_r1_hardtrimming
description: Use this skill when orchestrating the retained "ilmn_1b_R1_hardTrimming" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 1b R1 hardTrimming stage tied to upstream `ilmn_1b_cutadapt2` and the downstream handoff to `ilmn_1b_R1_internalTrimming`. It tracks completion via `results/finish/ilmn_1b_R1_hardTrimming.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_1b_R1_hardTrimming
  step_name: ilmn 1b R1 hardTrimming
---

# Scope
Use this skill only for the `ilmn_1b_R1_hardTrimming` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_1b_cutadapt2`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_1b_R1_hardTrimming.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_1b_R1_hardTrimming.done`
- Representative outputs: `results/finish/ilmn_1b_R1_hardTrimming.done`
- Execution targets: `ilmn_1b_R1_hardTrimming`
- Downstream handoff: `ilmn_1b_R1_internalTrimming`

## Guardrails
- Treat `results/finish/ilmn_1b_R1_hardTrimming.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_1b_R1_hardTrimming.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_1b_R1_internalTrimming` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_1b_R1_hardTrimming.done` exists and `ilmn_1b_R1_internalTrimming` can proceed without re-running ilmn 1b R1 hardTrimming.
