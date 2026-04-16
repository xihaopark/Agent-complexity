---
name: finish-joncahn-epigeneticbutton-make_srna_stranded_bigwigs
description: Use this skill when orchestrating the retained "make_srna_stranded_bigwigs" step of the joncahn epigeneticbutton finish finish workflow. It keeps the make srna stranded bigwigs stage tied to upstream `merging_srna_replicates` and the downstream handoff to `analyze_all_srna_samples_on_target_file`. It tracks completion via `results/finish/make_srna_stranded_bigwigs.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: make_srna_stranded_bigwigs
  step_name: make srna stranded bigwigs
---

# Scope
Use this skill only for the `make_srna_stranded_bigwigs` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `merging_srna_replicates`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/make_srna_stranded_bigwigs.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_srna_stranded_bigwigs.done`
- Representative outputs: `results/finish/make_srna_stranded_bigwigs.done`
- Execution targets: `make_srna_stranded_bigwigs`
- Downstream handoff: `analyze_all_srna_samples_on_target_file`

## Guardrails
- Treat `results/finish/make_srna_stranded_bigwigs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_srna_stranded_bigwigs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `analyze_all_srna_samples_on_target_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_srna_stranded_bigwigs.done` exists and `analyze_all_srna_samples_on_target_file` can proceed without re-running make srna stranded bigwigs.
