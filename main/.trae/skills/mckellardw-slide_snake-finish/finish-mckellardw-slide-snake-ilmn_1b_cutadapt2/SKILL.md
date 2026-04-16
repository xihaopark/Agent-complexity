---
name: finish-mckellardw-slide-snake-ilmn_1b_cutadapt2
description: Use this skill when orchestrating the retained "ilmn_1b_cutadapt2" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 1b cutadapt2 stage tied to upstream `ilmn_1b_cutadapt` and the downstream handoff to `ilmn_1b_R1_hardTrimming`. It tracks completion via `results/finish/ilmn_1b_cutadapt2.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_1b_cutadapt2
  step_name: ilmn 1b cutadapt2
---

# Scope
Use this skill only for the `ilmn_1b_cutadapt2` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_1b_cutadapt`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_1b_cutadapt2.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_1b_cutadapt2.done`
- Representative outputs: `results/finish/ilmn_1b_cutadapt2.done`
- Execution targets: `ilmn_1b_cutadapt2`
- Downstream handoff: `ilmn_1b_R1_hardTrimming`

## Guardrails
- Treat `results/finish/ilmn_1b_cutadapt2.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_1b_cutadapt2.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_1b_R1_hardTrimming` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_1b_cutadapt2.done` exists and `ilmn_1b_R1_hardTrimming` can proceed without re-running ilmn 1b cutadapt2.
