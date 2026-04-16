---
name: finish-mckellardw-slide-snake-ont_1b_cutadapt
description: Use this skill when orchestrating the retained "ont_1b_cutadapt" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 1b cutadapt stage tied to upstream `ont_1a_split_fastq_to_R1_R2` and the downstream handoff to `ont_1b_R1_hardTrimming`. It tracks completion via `results/finish/ont_1b_cutadapt.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_1b_cutadapt
  step_name: ont 1b cutadapt
---

# Scope
Use this skill only for the `ont_1b_cutadapt` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_1a_split_fastq_to_R1_R2`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_1b_cutadapt.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_1b_cutadapt.done`
- Representative outputs: `results/finish/ont_1b_cutadapt.done`
- Execution targets: `ont_1b_cutadapt`
- Downstream handoff: `ont_1b_R1_hardTrimming`

## Guardrails
- Treat `results/finish/ont_1b_cutadapt.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_1b_cutadapt.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_1b_R1_hardTrimming` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_1b_cutadapt.done` exists and `ont_1b_R1_hardTrimming` can proceed without re-running ont 1b cutadapt.
