---
name: finish-joncahn-epigeneticbutton-analyze_all_srna_samples_on_target_file
description: Use this skill when orchestrating the retained "analyze_all_srna_samples_on_target_file" step of the joncahn epigeneticbutton finish finish workflow. It keeps the analyze all srna samples on target file stage tied to upstream `make_srna_stranded_bigwigs` and the downstream handoff to `prep_files_for_differential_srna_clusters`. It tracks completion via `results/finish/analyze_all_srna_samples_on_target_file.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: analyze_all_srna_samples_on_target_file
  step_name: analyze all srna samples on target file
---

# Scope
Use this skill only for the `analyze_all_srna_samples_on_target_file` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_srna_stranded_bigwigs`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/analyze_all_srna_samples_on_target_file.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/analyze_all_srna_samples_on_target_file.done`
- Representative outputs: `results/finish/analyze_all_srna_samples_on_target_file.done`
- Execution targets: `analyze_all_srna_samples_on_target_file`
- Downstream handoff: `prep_files_for_differential_srna_clusters`

## Guardrails
- Treat `results/finish/analyze_all_srna_samples_on_target_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/analyze_all_srna_samples_on_target_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `prep_files_for_differential_srna_clusters` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/analyze_all_srna_samples_on_target_file.done` exists and `prep_files_for_differential_srna_clusters` can proceed without re-running analyze all srna samples on target file.
