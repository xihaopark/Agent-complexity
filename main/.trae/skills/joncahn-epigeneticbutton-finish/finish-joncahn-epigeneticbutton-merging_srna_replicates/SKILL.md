---
name: finish-joncahn-epigeneticbutton-merging_srna_replicates
description: Use this skill when orchestrating the retained "merging_srna_replicates" step of the joncahn epigeneticbutton finish finish workflow. It keeps the merging srna replicates stage tied to upstream `filter_size_srna_sample` and the downstream handoff to `make_srna_stranded_bigwigs`. It tracks completion via `results/finish/merging_srna_replicates.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: merging_srna_replicates
  step_name: merging srna replicates
---

# Scope
Use this skill only for the `merging_srna_replicates` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `filter_size_srna_sample`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/merging_srna_replicates.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merging_srna_replicates.done`
- Representative outputs: `results/finish/merging_srna_replicates.done`
- Execution targets: `merging_srna_replicates`
- Downstream handoff: `make_srna_stranded_bigwigs`

## Guardrails
- Treat `results/finish/merging_srna_replicates.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merging_srna_replicates.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_srna_stranded_bigwigs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merging_srna_replicates.done` exists and `make_srna_stranded_bigwigs` can proceed without re-running merging srna replicates.
