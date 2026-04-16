---
name: finish-joncahn-epigeneticbutton-making_pseudo_replicates
description: Use this skill when orchestrating the retained "making_pseudo_replicates" step of the joncahn epigeneticbutton finish finish workflow. It keeps the making pseudo replicates stage tied to upstream `merging_chip_replicates` and the downstream handoff to `create_empty_file`. It tracks completion via `results/finish/making_pseudo_replicates.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: making_pseudo_replicates
  step_name: making pseudo replicates
---

# Scope
Use this skill only for the `making_pseudo_replicates` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `merging_chip_replicates`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/making_pseudo_replicates.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/making_pseudo_replicates.done`
- Representative outputs: `results/finish/making_pseudo_replicates.done`
- Execution targets: `making_pseudo_replicates`
- Downstream handoff: `create_empty_file`

## Guardrails
- Treat `results/finish/making_pseudo_replicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/making_pseudo_replicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `create_empty_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/making_pseudo_replicates.done` exists and `create_empty_file` can proceed without re-running making pseudo replicates.
