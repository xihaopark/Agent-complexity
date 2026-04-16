---
name: finish-joncahn-epigeneticbutton-convert_bedmethyl_to_cx_report
description: Use this skill when orchestrating the retained "convert_bedmethyl_to_cx_report" step of the joncahn epigeneticbutton finish finish workflow. It keeps the convert bedmethyl to cx report stage tied to upstream `make_mc_stats_dmc` and the downstream handoff to `deduplicate_srna_nextflexv3`. It tracks completion via `results/finish/convert_bedmethyl_to_cx_report.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: convert_bedmethyl_to_cx_report
  step_name: convert bedmethyl to cx report
---

# Scope
Use this skill only for the `convert_bedmethyl_to_cx_report` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_mc_stats_dmc`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/convert_bedmethyl_to_cx_report.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/convert_bedmethyl_to_cx_report.done`
- Representative outputs: `results/finish/convert_bedmethyl_to_cx_report.done`
- Execution targets: `convert_bedmethyl_to_cx_report`
- Downstream handoff: `deduplicate_srna_nextflexv3`

## Guardrails
- Treat `results/finish/convert_bedmethyl_to_cx_report.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/convert_bedmethyl_to_cx_report.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `deduplicate_srna_nextflexv3` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/convert_bedmethyl_to_cx_report.done` exists and `deduplicate_srna_nextflexv3` can proceed without re-running convert bedmethyl to cx report.
