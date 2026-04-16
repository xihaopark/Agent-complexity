---
name: finish-joncahn-epigeneticbutton-make_srna_size_stats
description: Use this skill when orchestrating the retained "make_srna_size_stats" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make srna size stats stage tied to upstream `make_cluster_bedfiles` and the downstream handoff to `filter_size_srna_sample`. It tracks completion via `results/finish/make_srna_size_stats.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_srna_size_stats
  step_name: make srna size stats
---

# Scope
Use this skill only for the `make_srna_size_stats` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_cluster_bedfiles`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_srna_size_stats.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_srna_size_stats.done`
- Representative outputs: `results/finish/make_srna_size_stats.done`
- Execution targets: `make_srna_size_stats`
- Downstream handoff: `filter_size_srna_sample`

## Guardrails
- Treat `results/finish/make_srna_size_stats.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_srna_size_stats.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_size_srna_sample` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_srna_size_stats.done` exists and `filter_size_srna_sample` can proceed without re-running make srna size stats.
