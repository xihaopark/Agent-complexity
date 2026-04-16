---
name: finish-mckellardw-slide-snake-ilmn_2b_ribodetector_filter_r1
description: Use this skill when orchestrating the retained "ilmn_2b_ribodetector_filter_R1" step of the mckellardw slide_snake finish finish workflow. It keeps the ilmn 2b ribodetector filter R1 stage tied to upstream `ilmn_2b_ribodetector_get_no_rRNA_list` and the downstream handoff to `ilmn_2b_ribodetector_filter_trimmed_R1`. It tracks completion via `results/finish/ilmn_2b_ribodetector_filter_R1.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ilmn_2b_ribodetector_filter_R1
  step_name: ilmn 2b ribodetector filter R1
---

# Scope
Use this skill only for the `ilmn_2b_ribodetector_filter_R1` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ilmn_2b_ribodetector_get_no_rRNA_list`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ilmn_2b_ribodetector_filter_R1.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ilmn_2b_ribodetector_filter_R1.done`
- Representative outputs: `results/finish/ilmn_2b_ribodetector_filter_R1.done`
- Execution targets: `ilmn_2b_ribodetector_filter_R1`
- Downstream handoff: `ilmn_2b_ribodetector_filter_trimmed_R1`

## Guardrails
- Treat `results/finish/ilmn_2b_ribodetector_filter_R1.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ilmn_2b_ribodetector_filter_R1.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ilmn_2b_ribodetector_filter_trimmed_R1` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ilmn_2b_ribodetector_filter_R1.done` exists and `ilmn_2b_ribodetector_filter_trimmed_R1` can proceed without re-running ilmn 2b ribodetector filter R1.
