---
name: finish-joncahn-epigeneticbutton-perform_go_on_target_file
description: Use this skill when orchestrating the retained "perform_GO_on_target_file" step of the joncahn epigeneticbutton finish finish workflow. It keeps the perform GO on target file stage tied to upstream `create_GO_database` and the downstream handoff to `call_rampage_TSS`. It tracks completion via `results/finish/perform_GO_on_target_file.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: perform_GO_on_target_file
  step_name: perform GO on target file
---

# Scope
Use this skill only for the `perform_GO_on_target_file` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `create_GO_database`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/perform_GO_on_target_file.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/perform_GO_on_target_file.done`
- Representative outputs: `results/finish/perform_GO_on_target_file.done`
- Execution targets: `perform_GO_on_target_file`
- Downstream handoff: `call_rampage_TSS`

## Guardrails
- Treat `results/finish/perform_GO_on_target_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/perform_GO_on_target_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `call_rampage_TSS` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/perform_GO_on_target_file.done` exists and `call_rampage_TSS` can proceed without re-running perform GO on target file.
