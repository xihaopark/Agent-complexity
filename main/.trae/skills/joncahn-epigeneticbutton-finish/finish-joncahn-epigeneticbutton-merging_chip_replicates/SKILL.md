---
name: finish-joncahn-epigeneticbutton-merging_chip_replicates
description: Use this skill when orchestrating the retained "merging_chip_replicates" step of the joncahn epigeneticbutton finish finish workflow. It keeps the merging chip replicates stage tied to upstream `idr_analysis_replicates` and the downstream handoff to `making_pseudo_replicates`. It tracks completion via `results/finish/merging_chip_replicates.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: merging_chip_replicates
  step_name: merging chip replicates
---

# Scope
Use this skill only for the `merging_chip_replicates` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `idr_analysis_replicates`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/merging_chip_replicates.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merging_chip_replicates.done`
- Representative outputs: `results/finish/merging_chip_replicates.done`
- Execution targets: `merging_chip_replicates`
- Downstream handoff: `making_pseudo_replicates`

## Guardrails
- Treat `results/finish/merging_chip_replicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merging_chip_replicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `making_pseudo_replicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merging_chip_replicates.done` exists and `making_pseudo_replicates` can proceed without re-running merging chip replicates.
