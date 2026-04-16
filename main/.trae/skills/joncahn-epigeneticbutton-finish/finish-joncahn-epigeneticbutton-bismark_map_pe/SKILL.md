---
name: finish-joncahn-epigeneticbutton-bismark_map_pe
description: Use this skill when orchestrating the retained "bismark_map_pe" step of the joncahn epigeneticbutton finish finish workflow. It keeps the bismark map pe stage tied to upstream `make_bismark_indices` and the downstream handoff to `bismark_map_se`. It tracks completion via `results/finish/bismark_map_pe.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: bismark_map_pe
  step_name: bismark map pe
---

# Scope
Use this skill only for the `bismark_map_pe` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_bismark_indices`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/bismark_map_pe.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bismark_map_pe.done`
- Representative outputs: `results/finish/bismark_map_pe.done`
- Execution targets: `bismark_map_pe`
- Downstream handoff: `bismark_map_se`

## Guardrails
- Treat `results/finish/bismark_map_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bismark_map_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bismark_map_se` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bismark_map_pe.done` exists and `bismark_map_se` can proceed without re-running bismark map pe.
