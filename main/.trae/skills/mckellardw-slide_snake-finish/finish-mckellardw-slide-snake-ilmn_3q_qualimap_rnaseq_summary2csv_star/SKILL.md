---
name: finish-mckellardw-slide-snake-ilmn_3q_qualimap_rnaseq_summary2csv_star
description: Use this skill when orchestrating the retained "ilmn_3q_qualimap_rnaseq_summary2csv_STAR" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 3q qualimap rnaseq summary2csv STAR stage tied to upstream `ilmn_3q_qualimapQC_dedup_STAR` and the downstream handoff to `ilmn_3q_qualimap_bamqc_STAR_raw`. It tracks completion via `results/finish/ilmn_3q_qualimap_rnaseq_summary2csv_STAR.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_3q_qualimap_rnaseq_summary2csv_STAR
  step_name: ilmn 3q qualimap rnaseq summary2csv STAR
---

# Scope
Use this skill only for the `ilmn_3q_qualimap_rnaseq_summary2csv_STAR` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_3q_qualimapQC_dedup_STAR`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_3q_qualimap_rnaseq_summary2csv_STAR.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_3q_qualimap_rnaseq_summary2csv_STAR.done`
- Representative outputs: `results/finish/ilmn_3q_qualimap_rnaseq_summary2csv_STAR.done`
- Execution targets: `ilmn_3q_qualimap_rnaseq_summary2csv_STAR`
- Downstream handoff: `ilmn_3q_qualimap_bamqc_STAR_raw`

## Guardrails
- Treat `results/finish/ilmn_3q_qualimap_rnaseq_summary2csv_STAR.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_3q_qualimap_rnaseq_summary2csv_STAR.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_3q_qualimap_bamqc_STAR_raw` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_3q_qualimap_rnaseq_summary2csv_STAR.done` exists and `ilmn_3q_qualimap_bamqc_STAR_raw` can proceed without re-running ilmn 3q qualimap rnaseq summary2csv STAR.
