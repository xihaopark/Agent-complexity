---
name: finish-joncahn-epigeneticbutton-all_atac
description: Use this skill when orchestrating the retained "all_atac" step of the joncahn epigeneticbutton finish finish workflow. It keeps the all atac stage tied to upstream `make_coverage_atac` and the downstream handoff to `make_STAR_indices`. It tracks completion via `results/finish/all_atac.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: all_atac
  step_name: all atac
---

# Scope
Use this skill only for the `all_atac` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `make_coverage_atac`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/all_atac.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all_atac.done`
- Representative outputs: `results/finish/all_atac.done`
- Execution targets: `all_atac`
- Downstream handoff: `make_STAR_indices`

## Guardrails
- Treat `results/finish/all_atac.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all_atac.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `make_STAR_indices` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/all_atac.done` exists and `make_STAR_indices` can proceed without re-running all atac.
