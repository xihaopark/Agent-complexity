---
name: finish-joncahn-epigeneticbutton-merge_pileup_sources
description: Use this skill when orchestrating the retained "merge_pileup_sources" step of the joncahn epigeneticbutton finish finish workflow. It keeps the merge pileup sources stage tied to upstream `copy_bedmethyl_input` and the downstream handoff to `modkit_summary_dmc`. It tracks completion via `results/finish/merge_pileup_sources.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: merge_pileup_sources
  step_name: merge pileup sources
---

# Scope
Use this skill only for the `merge_pileup_sources` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `copy_bedmethyl_input`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/merge_pileup_sources.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/merge_pileup_sources.done`
- Representative outputs: `results/finish/merge_pileup_sources.done`
- Execution targets: `merge_pileup_sources`
- Downstream handoff: `modkit_summary_dmc`

## Guardrails
- Treat `results/finish/merge_pileup_sources.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/merge_pileup_sources.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `modkit_summary_dmc` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/merge_pileup_sources.done` exists and `modkit_summary_dmc` can proceed without re-running merge pileup sources.
