---
name: finish-joncahn-epigeneticbutton-has_header
description: Use this skill when orchestrating the retained "has_header" step of the joncahn epigeneticbutton finish finish workflow. It keeps the has header stage tied to upstream `all_srna` and the downstream handoff to `is_stranded`. It tracks completion via `results/finish/has_header.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: has_header
  step_name: has header
---

# Scope
Use this skill only for the `has_header` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `all_srna`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/has_header.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/has_header.done`
- Representative outputs: `results/finish/has_header.done`
- Execution targets: `has_header`
- Downstream handoff: `is_stranded`

## Guardrails
- Treat `results/finish/has_header.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/has_header.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `is_stranded` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/has_header.done` exists and `is_stranded` can proceed without re-running has header.
