---
name: finish-joncahn-epigeneticbutton-prep_files_for_degs
description: Use this skill when orchestrating the retained "prep_files_for_DEGs" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prep files for DEGs stage tied to upstream `make_rna_unstranded_bigwigs` and the downstream handoff to `call_all_DEGs`. It tracks completion via `results/finish/prep_files_for_DEGs.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prep_files_for_DEGs
  step_name: prep files for DEGs
---

# Scope
Use this skill only for the `prep_files_for_DEGs` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_rna_unstranded_bigwigs`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prep_files_for_DEGs.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prep_files_for_DEGs.done`
- Representative outputs: `results/finish/prep_files_for_DEGs.done`
- Execution targets: `prep_files_for_DEGs`
- Downstream handoff: `call_all_DEGs`

## Guardrails
- Treat `results/finish/prep_files_for_DEGs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prep_files_for_DEGs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `call_all_DEGs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prep_files_for_DEGs.done` exists and `call_all_DEGs` can proceed without re-running prep files for DEGs.
