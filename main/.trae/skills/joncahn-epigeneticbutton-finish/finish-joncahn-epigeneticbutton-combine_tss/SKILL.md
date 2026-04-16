---
name: finish-joncahn-epigeneticbutton-combine_tss
description: Use this skill when orchestrating the retained "combine_TSS" step of the joncahn epigeneticbutton finish finish workflow. It keeps the combine TSS stage tied to upstream `combine_peakfiles` and the downstream handoff to `get_annotations_for_bedfile`. It tracks completion via `results/finish/combine_TSS.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: combine_TSS
  step_name: combine TSS
---

# Scope
Use this skill only for the `combine_TSS` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `combine_peakfiles`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/combine_TSS.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/combine_TSS.done`
- Representative outputs: `results/finish/combine_TSS.done`
- Execution targets: `combine_TSS`
- Downstream handoff: `get_annotations_for_bedfile`

## Guardrails
- Treat `results/finish/combine_TSS.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/combine_TSS.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_annotations_for_bedfile` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/combine_TSS.done` exists and `get_annotations_for_bedfile` can proceed without re-running combine TSS.
