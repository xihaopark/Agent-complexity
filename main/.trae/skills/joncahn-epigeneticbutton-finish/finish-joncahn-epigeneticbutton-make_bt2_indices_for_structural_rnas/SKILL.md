---
name: finish-joncahn-epigeneticbutton-make_bt2_indices_for_structural_rnas
description: Use this skill when orchestrating the retained "make_bt2_indices_for_structural_RNAs" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make bt2 indices for structural RNAs stage tied to upstream `deduplicate_srna_nextflexv3` and the downstream handoff to `filter_structural_rna`. It tracks completion via `results/finish/make_bt2_indices_for_structural_RNAs.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_bt2_indices_for_structural_RNAs
  step_name: make bt2 indices for structural RNAs
---

# Scope
Use this skill only for the `make_bt2_indices_for_structural_RNAs` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `deduplicate_srna_nextflexv3`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_bt2_indices_for_structural_RNAs.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_bt2_indices_for_structural_RNAs.done`
- Representative outputs: `results/finish/make_bt2_indices_for_structural_RNAs.done`
- Execution targets: `make_bt2_indices_for_structural_RNAs`
- Downstream handoff: `filter_structural_rna`

## Guardrails
- Treat `results/finish/make_bt2_indices_for_structural_RNAs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_bt2_indices_for_structural_RNAs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `filter_structural_rna` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_bt2_indices_for_structural_RNAs.done` exists and `filter_structural_rna` can proceed without re-running make bt2 indices for structural RNAs.
