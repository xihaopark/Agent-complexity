---
name: finish-joncahn-epigeneticbutton-merging_mc_replicates
description: Use this skill when orchestrating the retained "merging_mc_replicates" step of the joncahn epigeneticbutton finish finish workflow. It keeps the merging mc replicates stage tied to upstream `make_mc_stats_se` and the downstream handoff to `make_mc_bigwig_files`. It tracks completion via `results/finish/merging_mc_replicates.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: merging_mc_replicates
  step_name: merging mc replicates
---

# Scope
Use this skill only for the `merging_mc_replicates` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_mc_stats_se`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/merging_mc_replicates.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merging_mc_replicates.done`
- Representative outputs: `results/finish/merging_mc_replicates.done`
- Execution targets: `merging_mc_replicates`
- Downstream handoff: `make_mc_bigwig_files`

## Guardrails
- Treat `results/finish/merging_mc_replicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merging_mc_replicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_mc_bigwig_files` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merging_mc_replicates.done` exists and `make_mc_bigwig_files` can proceed without re-running merging mc replicates.
