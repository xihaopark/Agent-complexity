---
name: finish-mckellardw-slide-snake-ilmn_2a_bwa_rrna_get_no_rrna_list
description: Use this skill when orchestrating the retained "ilmn_2a_bwa_rRNA_get_no_rRNA_list" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2a bwa rRNA get no rRNA list stage tied to upstream `ilmn_2a_bwa_rRNA_align` and the downstream handoff to `ilmn_2a_bwa_rRNA_filter_R1`. It tracks completion via `results/finish/ilmn_2a_bwa_rRNA_get_no_rRNA_list.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2a_bwa_rRNA_get_no_rRNA_list
  step_name: ilmn 2a bwa rRNA get no rRNA list
---

# Scope
Use this skill only for the `ilmn_2a_bwa_rRNA_get_no_rRNA_list` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2a_bwa_rRNA_align`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2a_bwa_rRNA_get_no_rRNA_list.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2a_bwa_rRNA_get_no_rRNA_list.done`
- Representative outputs: `results/finish/ilmn_2a_bwa_rRNA_get_no_rRNA_list.done`
- Execution targets: `ilmn_2a_bwa_rRNA_get_no_rRNA_list`
- Downstream handoff: `ilmn_2a_bwa_rRNA_filter_R1`

## Guardrails
- Treat `results/finish/ilmn_2a_bwa_rRNA_get_no_rRNA_list.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2a_bwa_rRNA_get_no_rRNA_list.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2a_bwa_rRNA_filter_R1` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2a_bwa_rRNA_get_no_rRNA_list.done` exists and `ilmn_2a_bwa_rRNA_filter_R1` can proceed without re-running ilmn 2a bwa rRNA get no rRNA list.
