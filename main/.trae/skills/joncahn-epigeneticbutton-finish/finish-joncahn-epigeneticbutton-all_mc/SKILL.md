---
name: finish-joncahn-epigeneticbutton-all_mc
description: Use this skill when orchestrating the retained "all_mc" step of the joncahn epigeneticbutton finish finish workflow. It keeps the all mc stage tied to upstream `call_DMRs_pairwise` and the downstream handoff to `download_modkit`. It tracks completion via `results/finish/all_mc.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: all_mc
  step_name: all mc
---

# Scope
Use this skill only for the `all_mc` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `call_DMRs_pairwise`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/all_mc.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all_mc.done`
- Representative outputs: `results/finish/all_mc.done`
- Execution targets: `all_mc`
- Downstream handoff: `download_modkit`

## Guardrails
- Treat `results/finish/all_mc.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all_mc.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `download_modkit` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/all_mc.done` exists and `download_modkit` can proceed without re-running all mc.
