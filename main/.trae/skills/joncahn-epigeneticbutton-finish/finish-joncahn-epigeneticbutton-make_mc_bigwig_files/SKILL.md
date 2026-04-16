---
name: finish-joncahn-epigeneticbutton-make_mc_bigwig_files
description: Use this skill when orchestrating the retained "make_mc_bigwig_files" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make mc bigwig files stage tied to upstream `merging_mc_replicates` and the downstream handoff to `call_DMRs_pairwise`. It tracks completion via `results/finish/make_mc_bigwig_files.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_mc_bigwig_files
  step_name: make mc bigwig files
---

# Scope
Use this skill only for the `make_mc_bigwig_files` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `merging_mc_replicates`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_mc_bigwig_files.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_mc_bigwig_files.done`
- Representative outputs: `results/finish/make_mc_bigwig_files.done`
- Execution targets: `make_mc_bigwig_files`
- Downstream handoff: `call_DMRs_pairwise`

## Guardrails
- Treat `results/finish/make_mc_bigwig_files.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_mc_bigwig_files.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `call_DMRs_pairwise` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_mc_bigwig_files.done` exists and `call_DMRs_pairwise` can proceed without re-running make mc bigwig files.
