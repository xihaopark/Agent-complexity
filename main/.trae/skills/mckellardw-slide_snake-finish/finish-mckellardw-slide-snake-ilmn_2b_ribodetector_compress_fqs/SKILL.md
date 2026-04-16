---
name: finish-mckellardw-slide-snake-ilmn_2b_ribodetector_compress_fqs
description: Use this skill when orchestrating the retained "ilmn_2b_ribodetector_compress_fqs" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2b ribodetector compress fqs stage tied to upstream `ilmn_2b_ribodetector_filter_trimmed_R1` and the downstream handoff to `ilmn_2c_qualimapQC_rRNA_bwa`. It tracks completion via `results/finish/ilmn_2b_ribodetector_compress_fqs.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2b_ribodetector_compress_fqs
  step_name: ilmn 2b ribodetector compress fqs
---

# Scope
Use this skill only for the `ilmn_2b_ribodetector_compress_fqs` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2b_ribodetector_filter_trimmed_R1`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2b_ribodetector_compress_fqs.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2b_ribodetector_compress_fqs.done`
- Representative outputs: `results/finish/ilmn_2b_ribodetector_compress_fqs.done`
- Execution targets: `ilmn_2b_ribodetector_compress_fqs`
- Downstream handoff: `ilmn_2c_qualimapQC_rRNA_bwa`

## Guardrails
- Treat `results/finish/ilmn_2b_ribodetector_compress_fqs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2b_ribodetector_compress_fqs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2c_qualimapQC_rRNA_bwa` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2b_ribodetector_compress_fqs.done` exists and `ilmn_2c_qualimapQC_rRNA_bwa` can proceed without re-running ilmn 2b ribodetector compress fqs.
