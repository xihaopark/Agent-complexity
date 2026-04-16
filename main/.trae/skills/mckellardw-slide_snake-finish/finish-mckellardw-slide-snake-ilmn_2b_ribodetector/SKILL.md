---
name: finish-mckellardw-slide-snake-ilmn_2b_ribodetector
description: Use this skill when orchestrating the retained "ilmn_2b_ribodetector" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2b ribodetector stage tied to upstream `ilmn_2a_bwa_rRNA_filtered_fastqc` and the downstream handoff to `ilmn_2b_ribodetector_get_no_rRNA_list`. It tracks completion via `results/finish/ilmn_2b_ribodetector.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2b_ribodetector
  step_name: ilmn 2b ribodetector
---

# Scope
Use this skill only for the `ilmn_2b_ribodetector` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2a_bwa_rRNA_filtered_fastqc`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2b_ribodetector.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2b_ribodetector.done`
- Representative outputs: `results/finish/ilmn_2b_ribodetector.done`
- Execution targets: `ilmn_2b_ribodetector`
- Downstream handoff: `ilmn_2b_ribodetector_get_no_rRNA_list`

## Guardrails
- Treat `results/finish/ilmn_2b_ribodetector.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2b_ribodetector.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2b_ribodetector_get_no_rRNA_list` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2b_ribodetector.done` exists and `ilmn_2b_ribodetector_get_no_rRNA_list` can proceed without re-running ilmn 2b ribodetector.
