---
name: finish-joncahn-epigeneticbutton-filter_size_srna_sample
description: Use this skill when orchestrating the retained "filter_size_srna_sample" step of the joncahn epigeneticbutton finish finish workflow. It keeps the filter size srna sample stage tied to upstream `make_srna_size_stats` and the downstream handoff to `merging_srna_replicates`. It tracks completion via `results/finish/filter_size_srna_sample.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: filter_size_srna_sample
  step_name: filter size srna sample
---

# Scope
Use this skill only for the `filter_size_srna_sample` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_srna_size_stats`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/filter_size_srna_sample.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_size_srna_sample.done`
- Representative outputs: `results/finish/filter_size_srna_sample.done`
- Execution targets: `filter_size_srna_sample`
- Downstream handoff: `merging_srna_replicates`

## Guardrails
- Treat `results/finish/filter_size_srna_sample.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_size_srna_sample.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merging_srna_replicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_size_srna_sample.done` exists and `merging_srna_replicates` can proceed without re-running filter size srna sample.
