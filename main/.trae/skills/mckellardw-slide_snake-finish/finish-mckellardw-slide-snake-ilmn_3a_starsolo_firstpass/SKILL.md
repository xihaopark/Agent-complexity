---
name: finish-mckellardw-slide-snake-ilmn_3a_starsolo_firstpass
description: Use this skill when orchestrating the retained "ilmn_3a_STARsolo_firstPass" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3a STARsolo firstPass stage tied to upstream `ilmn_2c_qualimap_bamqc_summary2csv_rRNA_bwa` and the downstream handoff to `ilmn_3a_STARsolo_secondPass`. It tracks completion via `results/finish/ilmn_3a_STARsolo_firstPass.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3a_STARsolo_firstPass
  step_name: ilmn 3a STARsolo firstPass
---

# Scope
Use this skill only for the `ilmn_3a_STARsolo_firstPass` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2c_qualimap_bamqc_summary2csv_rRNA_bwa`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3a_STARsolo_firstPass.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3a_STARsolo_firstPass.done`
- Representative outputs: `results/finish/ilmn_3a_STARsolo_firstPass.done`
- Execution targets: `ilmn_3a_STARsolo_firstPass`
- Downstream handoff: `ilmn_3a_STARsolo_secondPass`

## Guardrails
- Treat `results/finish/ilmn_3a_STARsolo_firstPass.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3a_STARsolo_firstPass.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3a_STARsolo_secondPass` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3a_STARsolo_firstPass.done` exists and `ilmn_3a_STARsolo_secondPass` can proceed without re-running ilmn 3a STARsolo firstPass.
