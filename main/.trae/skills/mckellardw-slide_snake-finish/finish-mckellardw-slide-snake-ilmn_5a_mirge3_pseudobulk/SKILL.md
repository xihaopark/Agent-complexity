---
name: finish-mckellardw-slide-snake-ilmn_5a_mirge3_pseudobulk
description: Use this skill when orchestrating the retained "ilmn_5a_miRge3_pseudobulk" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 5a miRge3 pseudobulk stage tied to upstream `ilmn_5a_copy_R2_fq_for_mirge` and the downstream handoff to `ilmn_7a_fastQC_preTrim`. It tracks completion via `results/finish/ilmn_5a_miRge3_pseudobulk.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_5a_miRge3_pseudobulk
  step_name: ilmn 5a miRge3 pseudobulk
---

# Scope
Use this skill only for the `ilmn_5a_miRge3_pseudobulk` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_5a_copy_R2_fq_for_mirge`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_5a_miRge3_pseudobulk.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_5a_miRge3_pseudobulk.done`
- Representative outputs: `results/finish/ilmn_5a_miRge3_pseudobulk.done`
- Execution targets: `ilmn_5a_miRge3_pseudobulk`
- Downstream handoff: `ilmn_7a_fastQC_preTrim`

## Guardrails
- Treat `results/finish/ilmn_5a_miRge3_pseudobulk.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_5a_miRge3_pseudobulk.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_7a_fastQC_preTrim` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_5a_miRge3_pseudobulk.done` exists and `ilmn_7a_fastQC_preTrim` can proceed without re-running ilmn 5a miRge3 pseudobulk.
