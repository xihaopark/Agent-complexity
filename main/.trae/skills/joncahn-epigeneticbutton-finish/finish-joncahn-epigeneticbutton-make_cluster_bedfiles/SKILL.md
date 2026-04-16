---
name: finish-joncahn-epigeneticbutton-make_cluster_bedfiles
description: Use this skill when orchestrating the retained "make_cluster_bedfiles" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make cluster bedfiles stage tied to upstream `shortstack_map` and the downstream handoff to `make_srna_size_stats`. It tracks completion via `results/finish/make_cluster_bedfiles.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_cluster_bedfiles
  step_name: make cluster bedfiles
---

# Scope
Use this skill only for the `make_cluster_bedfiles` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `shortstack_map`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_cluster_bedfiles.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_cluster_bedfiles.done`
- Representative outputs: `results/finish/make_cluster_bedfiles.done`
- Execution targets: `make_cluster_bedfiles`
- Downstream handoff: `make_srna_size_stats`

## Guardrails
- Treat `results/finish/make_cluster_bedfiles.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_cluster_bedfiles.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_srna_size_stats` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_cluster_bedfiles.done` exists and `make_srna_size_stats` can proceed without re-running make cluster bedfiles.
