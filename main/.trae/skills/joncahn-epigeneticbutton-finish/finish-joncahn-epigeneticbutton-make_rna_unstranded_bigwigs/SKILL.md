---
name: finish-joncahn-epigeneticbutton-make_rna_unstranded_bigwigs
description: Use this skill when orchestrating the retained "make_rna_unstranded_bigwigs" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make rna unstranded bigwigs stage tied to upstream `make_rna_stranded_bigwigs` and the downstream handoff to `prep_files_for_DEGs`. It tracks completion via `results/finish/make_rna_unstranded_bigwigs.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_rna_unstranded_bigwigs
  step_name: make rna unstranded bigwigs
---

# Scope
Use this skill only for the `make_rna_unstranded_bigwigs` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_rna_stranded_bigwigs`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_rna_unstranded_bigwigs.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_rna_unstranded_bigwigs.done`
- Representative outputs: `results/finish/make_rna_unstranded_bigwigs.done`
- Execution targets: `make_rna_unstranded_bigwigs`
- Downstream handoff: `prep_files_for_DEGs`

## Guardrails
- Treat `results/finish/make_rna_unstranded_bigwigs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_rna_unstranded_bigwigs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prep_files_for_DEGs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_rna_unstranded_bigwigs.done` exists and `prep_files_for_DEGs` can proceed without re-running make rna unstranded bigwigs.
