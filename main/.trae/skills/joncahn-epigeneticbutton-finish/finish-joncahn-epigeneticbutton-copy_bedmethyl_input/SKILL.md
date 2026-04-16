---
name: finish-joncahn-epigeneticbutton-copy_bedmethyl_input
description: Use this skill when orchestrating the retained "copy_bedmethyl_input" step of the joncahn epigeneticbutton finish finish workflow. It keeps the copy bedmethyl input stage tied to upstream `modkit_pileup_dmc` and the downstream handoff to `merge_pileup_sources`. It tracks completion via `results/finish/copy_bedmethyl_input.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: copy_bedmethyl_input
  step_name: copy bedmethyl input
---

# Scope
Use this skill only for the `copy_bedmethyl_input` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `modkit_pileup_dmc`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/copy_bedmethyl_input.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/copy_bedmethyl_input.done`
- Representative outputs: `results/finish/copy_bedmethyl_input.done`
- Execution targets: `copy_bedmethyl_input`
- Downstream handoff: `merge_pileup_sources`

## Guardrails
- Treat `results/finish/copy_bedmethyl_input.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/copy_bedmethyl_input.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_pileup_sources` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/copy_bedmethyl_input.done` exists and `merge_pileup_sources` can proceed without re-running copy bedmethyl input.
