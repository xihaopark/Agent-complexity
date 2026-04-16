---
name: finish-joncahn-epigeneticbutton-get_annotations_for_bedfile
description: Use this skill when orchestrating the retained "get_annotations_for_bedfile" step of the joncahn epigeneticbutton finish finish workflow. It keeps the get annotations for bedfile stage tied to upstream `combine_TSS` and the downstream handoff to `plotting_upset_regions`. It tracks completion via `results/finish/get_annotations_for_bedfile.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: get_annotations_for_bedfile
  step_name: get annotations for bedfile
---

# Scope
Use this skill only for the `get_annotations_for_bedfile` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `combine_TSS`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/get_annotations_for_bedfile.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_annotations_for_bedfile.done`
- Representative outputs: `results/finish/get_annotations_for_bedfile.done`
- Execution targets: `get_annotations_for_bedfile`
- Downstream handoff: `plotting_upset_regions`

## Guardrails
- Treat `results/finish/get_annotations_for_bedfile.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_annotations_for_bedfile.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plotting_upset_regions` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_annotations_for_bedfile.done` exists and `plotting_upset_regions` can proceed without re-running get annotations for bedfile.
