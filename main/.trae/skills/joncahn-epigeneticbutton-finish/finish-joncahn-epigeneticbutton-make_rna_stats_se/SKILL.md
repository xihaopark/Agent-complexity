---
name: finish-joncahn-epigeneticbutton-make_rna_stats_se
description: Use this skill when orchestrating the retained "make_rna_stats_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make rna stats se stage tied to upstream `make_rna_stats_pe` and the downstream handoff to `pe_or_se_rna_dispatch`. It tracks completion via `results/finish/make_rna_stats_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_rna_stats_se
  step_name: make rna stats se
---

# Scope
Use this skill only for the `make_rna_stats_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_rna_stats_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_rna_stats_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_rna_stats_se.done`
- Representative outputs: `results/finish/make_rna_stats_se.done`
- Execution targets: `make_rna_stats_se`
- Downstream handoff: `pe_or_se_rna_dispatch`

## Guardrails
- Treat `results/finish/make_rna_stats_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_rna_stats_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pe_or_se_rna_dispatch` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_rna_stats_se.done` exists and `pe_or_se_rna_dispatch` can proceed without re-running make rna stats se.
