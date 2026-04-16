---
name: finish-joncahn-epigeneticbutton-merging_rna_replicates
description: Use this skill when orchestrating the retained "merging_rna_replicates" step of the joncahn epigeneticbutton finish finish workflow. It keeps the merging rna replicates stage tied to upstream `pe_or_se_rna_dispatch` and the downstream handoff to `make_rna_stranded_bigwigs`. It tracks completion via `results/finish/merging_rna_replicates.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: merging_rna_replicates
  step_name: merging rna replicates
---

# Scope
Use this skill only for the `merging_rna_replicates` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `pe_or_se_rna_dispatch`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/merging_rna_replicates.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merging_rna_replicates.done`
- Representative outputs: `results/finish/merging_rna_replicates.done`
- Execution targets: `merging_rna_replicates`
- Downstream handoff: `make_rna_stranded_bigwigs`

## Guardrails
- Treat `results/finish/merging_rna_replicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merging_rna_replicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_rna_stranded_bigwigs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merging_rna_replicates.done` exists and `make_rna_stranded_bigwigs` can proceed without re-running merging rna replicates.
