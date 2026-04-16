---
name: finish-joncahn-epigeneticbutton-prep_files_for_differential_srna_clusters
description: Use this skill when orchestrating the retained "prep_files_for_differential_srna_clusters" step of the joncahn epigeneticbutton finish finish workflow. It keeps the prep files for differential srna clusters stage tied to upstream `analyze_all_srna_samples_on_target_file` and the downstream handoff to `call_all_differential_srna_clusters`. It tracks completion via `results/finish/prep_files_for_differential_srna_clusters.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: prep_files_for_differential_srna_clusters
  step_name: prep files for differential srna clusters
---

# Scope
Use this skill only for the `prep_files_for_differential_srna_clusters` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `analyze_all_srna_samples_on_target_file`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/prep_files_for_differential_srna_clusters.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prep_files_for_differential_srna_clusters.done`
- Representative outputs: `results/finish/prep_files_for_differential_srna_clusters.done`
- Execution targets: `prep_files_for_differential_srna_clusters`
- Downstream handoff: `call_all_differential_srna_clusters`

## Guardrails
- Treat `results/finish/prep_files_for_differential_srna_clusters.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/prep_files_for_differential_srna_clusters.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `call_all_differential_srna_clusters` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/prep_files_for_differential_srna_clusters.done` exists and `call_all_differential_srna_clusters` can proceed without re-running prep files for differential srna clusters.
