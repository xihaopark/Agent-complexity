---
name: finish-mckellardw-slide-snake-ilmn_5a_copy_r2_fq_for_mirge
description: Use this skill when orchestrating the retained "ilmn_5a_copy_R2_fq_for_mirge" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 5a copy R2 fq for mirge stage tied to upstream `ilmn_4a_cache_h5ad_kbpython_std` and the downstream handoff to `ilmn_5a_miRge3_pseudobulk`. It tracks completion via `results/finish/ilmn_5a_copy_R2_fq_for_mirge.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_5a_copy_R2_fq_for_mirge
  step_name: ilmn 5a copy R2 fq for mirge
---

# Scope
Use this skill only for the `ilmn_5a_copy_R2_fq_for_mirge` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_4a_cache_h5ad_kbpython_std`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_5a_copy_R2_fq_for_mirge.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_5a_copy_R2_fq_for_mirge.done`
- Representative outputs: `results/finish/ilmn_5a_copy_R2_fq_for_mirge.done`
- Execution targets: `ilmn_5a_copy_R2_fq_for_mirge`
- Downstream handoff: `ilmn_5a_miRge3_pseudobulk`

## Guardrails
- Treat `results/finish/ilmn_5a_copy_R2_fq_for_mirge.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_5a_copy_R2_fq_for_mirge.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_5a_miRge3_pseudobulk` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_5a_copy_R2_fq_for_mirge.done` exists and `ilmn_5a_miRge3_pseudobulk` can proceed without re-running ilmn 5a copy R2 fq for mirge.
