---
name: finish-joncahn-epigeneticbutton-call_all_differential_srna_clusters
description: Use this skill when orchestrating the retained "call_all_differential_srna_clusters" step of the joncahn epigeneticbutton finish finish workflow. It keeps the call all differential srna clusters stage tied to upstream `prep_files_for_differential_srna_clusters` and the downstream handoff to `all_srna`. It tracks completion via `results/finish/call_all_differential_srna_clusters.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: call_all_differential_srna_clusters
  step_name: call all differential srna clusters
---

# Scope
Use this skill only for the `call_all_differential_srna_clusters` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prep_files_for_differential_srna_clusters`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/call_all_differential_srna_clusters.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/call_all_differential_srna_clusters.done`
- Representative outputs: `results/finish/call_all_differential_srna_clusters.done`
- Execution targets: `call_all_differential_srna_clusters`
- Downstream handoff: `all_srna`

## Guardrails
- Treat `results/finish/call_all_differential_srna_clusters.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/call_all_differential_srna_clusters.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all_srna` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/call_all_differential_srna_clusters.done` exists and `all_srna` can proceed without re-running call all differential srna clusters.
