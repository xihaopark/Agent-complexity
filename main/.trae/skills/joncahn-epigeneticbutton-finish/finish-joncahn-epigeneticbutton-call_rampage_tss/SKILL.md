---
name: finish-joncahn-epigeneticbutton-call_rampage_tss
description: Use this skill when orchestrating the retained "call_rampage_TSS" step of the joncahn epigeneticbutton finish finish workflow. It keeps the call rampage TSS stage tied to upstream `perform_GO_on_target_file` and the downstream handoff to `all_rna`. It tracks completion via `results/finish/call_rampage_TSS.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: call_rampage_TSS
  step_name: call rampage TSS
---

# Scope
Use this skill only for the `call_rampage_TSS` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `perform_GO_on_target_file`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/call_rampage_TSS.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/call_rampage_TSS.done`
- Representative outputs: `results/finish/call_rampage_TSS.done`
- Execution targets: `call_rampage_TSS`
- Downstream handoff: `all_rna`

## Guardrails
- Treat `results/finish/call_rampage_TSS.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/call_rampage_TSS.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all_rna` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/call_rampage_TSS.done` exists and `all_rna` can proceed without re-running call rampage TSS.
