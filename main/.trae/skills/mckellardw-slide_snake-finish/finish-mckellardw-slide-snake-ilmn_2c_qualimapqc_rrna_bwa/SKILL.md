---
name: finish-mckellardw-slide-snake-ilmn_2c_qualimapqc_rrna_bwa
description: Use this skill when orchestrating the retained "ilmn_2c_qualimapQC_rRNA_bwa" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2c qualimapQC rRNA bwa stage tied to upstream `ilmn_2b_ribodetector_compress_fqs` and the downstream handoff to `ilmn_2c_qualimap_readqc_summary2csv_rRNA_bwa`. It tracks completion via `results/finish/ilmn_2c_qualimapQC_rRNA_bwa.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2c_qualimapQC_rRNA_bwa
  step_name: ilmn 2c qualimapQC rRNA bwa
---

# Scope
Use this skill only for the `ilmn_2c_qualimapQC_rRNA_bwa` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2b_ribodetector_compress_fqs`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2c_qualimapQC_rRNA_bwa.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2c_qualimapQC_rRNA_bwa.done`
- Representative outputs: `results/finish/ilmn_2c_qualimapQC_rRNA_bwa.done`
- Execution targets: `ilmn_2c_qualimapQC_rRNA_bwa`
- Downstream handoff: `ilmn_2c_qualimap_readqc_summary2csv_rRNA_bwa`

## Guardrails
- Treat `results/finish/ilmn_2c_qualimapQC_rRNA_bwa.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2c_qualimapQC_rRNA_bwa.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2c_qualimap_readqc_summary2csv_rRNA_bwa` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2c_qualimapQC_rRNA_bwa.done` exists and `ilmn_2c_qualimap_readqc_summary2csv_rRNA_bwa` can proceed without re-running ilmn 2c qualimapQC rRNA bwa.
