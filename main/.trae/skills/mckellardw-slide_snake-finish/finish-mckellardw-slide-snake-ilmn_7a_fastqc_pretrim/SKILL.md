---
name: finish-mckellardw-slide-snake-ilmn_7a_fastqc_pretrim
description: Use this skill when orchestrating the retained "ilmn_7a_fastQC_preTrim" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 7a fastQC preTrim stage tied to upstream `ilmn_5a_miRge3_pseudobulk` and the downstream handoff to `ilmn_7a_fastQC_postTrim`. It tracks completion via `results/finish/ilmn_7a_fastQC_preTrim.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_7a_fastQC_preTrim
  step_name: ilmn 7a fastQC preTrim
---

# Scope
Use this skill only for the `ilmn_7a_fastQC_preTrim` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_5a_miRge3_pseudobulk`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_7a_fastQC_preTrim.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_7a_fastQC_preTrim.done`
- Representative outputs: `results/finish/ilmn_7a_fastQC_preTrim.done`
- Execution targets: `ilmn_7a_fastQC_preTrim`
- Downstream handoff: `ilmn_7a_fastQC_postTrim`

## Guardrails
- Treat `results/finish/ilmn_7a_fastQC_preTrim.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_7a_fastQC_preTrim.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_7a_fastQC_postTrim` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_7a_fastQC_preTrim.done` exists and `ilmn_7a_fastQC_postTrim` can proceed without re-running ilmn 7a fastQC preTrim.
