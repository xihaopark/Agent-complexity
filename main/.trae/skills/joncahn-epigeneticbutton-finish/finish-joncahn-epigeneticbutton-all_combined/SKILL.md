---
name: finish-joncahn-epigeneticbutton-all_combined
description: Use this skill when orchestrating the retained "all_combined" step of the joncahn epigeneticbutton finish finish workflow. It keeps the all combined stage tied to upstream `plot_PCA_correlation` and the downstream handoff to `all`. It tracks completion via `results/finish/all_combined.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: all_combined
  step_name: all combined
---

# Scope
Use this skill only for the `all_combined` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `plot_PCA_correlation`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/all_combined.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all_combined.done`
- Representative outputs: `results/finish/all_combined.done`
- Execution targets: `all_combined`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/all_combined.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all_combined.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/all_combined.done` exists and `all` can proceed without re-running all combined.
