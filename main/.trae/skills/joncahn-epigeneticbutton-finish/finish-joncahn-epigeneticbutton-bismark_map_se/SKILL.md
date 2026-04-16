---
name: finish-joncahn-epigeneticbutton-bismark_map_se
description: Use this skill when orchestrating the retained "bismark_map_se" step of the joncahn epigeneticbutton finish finish workflow. It keeps the bismark map se stage tied to upstream `bismark_map_pe` and the downstream handoff to `pe_or_se_mc_dispatch`. It tracks completion via `results/finish/bismark_map_se.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: bismark_map_se
  step_name: bismark map se
---

# Scope
Use this skill only for the `bismark_map_se` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `bismark_map_pe`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/bismark_map_se.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bismark_map_se.done`
- Representative outputs: `results/finish/bismark_map_se.done`
- Execution targets: `bismark_map_se`
- Downstream handoff: `pe_or_se_mc_dispatch`

## Guardrails
- Treat `results/finish/bismark_map_se.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bismark_map_se.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `pe_or_se_mc_dispatch` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bismark_map_se.done` exists and `pe_or_se_mc_dispatch` can proceed without re-running bismark map se.
