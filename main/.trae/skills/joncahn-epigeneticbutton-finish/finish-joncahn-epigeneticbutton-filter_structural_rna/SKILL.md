---
name: finish-joncahn-epigeneticbutton-filter_structural_rna
description: Use this skill when orchestrating the retained "filter_structural_rna" step of the joncahn epigeneticbutton finish finish workflow. It keeps the filter structural rna stage tied to upstream `make_bt2_indices_for_structural_RNAs` and the downstream handoff to `dispatch_srna_fastq`. It tracks completion via `results/finish/filter_structural_rna.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: filter_structural_rna
  step_name: filter structural rna
---

# Scope
Use this skill only for the `filter_structural_rna` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_bt2_indices_for_structural_RNAs`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/filter_structural_rna.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_structural_rna.done`
- Representative outputs: `results/finish/filter_structural_rna.done`
- Execution targets: `filter_structural_rna`
- Downstream handoff: `dispatch_srna_fastq`

## Guardrails
- Treat `results/finish/filter_structural_rna.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_structural_rna.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `dispatch_srna_fastq` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_structural_rna.done` exists and `dispatch_srna_fastq` can proceed without re-running filter structural rna.
