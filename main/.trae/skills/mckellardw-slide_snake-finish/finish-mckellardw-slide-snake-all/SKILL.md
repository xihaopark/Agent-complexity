---
name: finish-mckellardw-slide-snake-all
description: Use this skill when orchestrating the retained "all" step of the mckellardw slide_snake finish finish workflow. It keeps the all stage tied to upstream `ont_3b_qualimap_bamqc_summary2csv`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_3b_qualimap_bamqc_summary2csv`
- Step file: `finish/mckellardw-slide_snake-finish/steps/all.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
