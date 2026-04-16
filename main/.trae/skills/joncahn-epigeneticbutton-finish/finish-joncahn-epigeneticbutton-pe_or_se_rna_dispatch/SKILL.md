---
name: finish-joncahn-epigeneticbutton-pe_or_se_rna_dispatch
description: Use this skill when orchestrating the retained "pe_or_se_rna_dispatch" step of the joncahn epigeneticbutton finish finish workflow. It keeps the pe or se rna dispatch stage tied to upstream `make_rna_stats_se` and the downstream handoff to `merging_rna_replicates`. It tracks completion via `results/finish/pe_or_se_rna_dispatch.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: pe_or_se_rna_dispatch
  step_name: pe or se rna dispatch
---

# Scope
Use this skill only for the `pe_or_se_rna_dispatch` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_rna_stats_se`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/pe_or_se_rna_dispatch.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/pe_or_se_rna_dispatch.done`
- Representative outputs: `results/finish/pe_or_se_rna_dispatch.done`
- Execution targets: `pe_or_se_rna_dispatch`
- Downstream handoff: `merging_rna_replicates`

## Guardrails
- Treat `results/finish/pe_or_se_rna_dispatch.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/pe_or_se_rna_dispatch.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merging_rna_replicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/pe_or_se_rna_dispatch.done` exists and `merging_rna_replicates` can proceed without re-running pe or se rna dispatch.
