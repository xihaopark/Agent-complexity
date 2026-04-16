---
name: finish-joncahn-epigeneticbutton-make_rna_stranded_bigwigs
description: Use this skill when orchestrating the retained "make_rna_stranded_bigwigs" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make rna stranded bigwigs stage tied to upstream `merging_rna_replicates` and the downstream handoff to `make_rna_unstranded_bigwigs`. It tracks completion via `results/finish/make_rna_stranded_bigwigs.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_rna_stranded_bigwigs
  step_name: make rna stranded bigwigs
---

# Scope
Use this skill only for the `make_rna_stranded_bigwigs` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `merging_rna_replicates`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_rna_stranded_bigwigs.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_rna_stranded_bigwigs.done`
- Representative outputs: `results/finish/make_rna_stranded_bigwigs.done`
- Execution targets: `make_rna_stranded_bigwigs`
- Downstream handoff: `make_rna_unstranded_bigwigs`

## Guardrails
- Treat `results/finish/make_rna_stranded_bigwigs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_rna_stranded_bigwigs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_rna_unstranded_bigwigs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_rna_stranded_bigwigs.done` exists and `make_rna_unstranded_bigwigs` can proceed without re-running make rna stranded bigwigs.
