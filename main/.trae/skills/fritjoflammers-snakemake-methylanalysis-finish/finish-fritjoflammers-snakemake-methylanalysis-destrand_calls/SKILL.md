---
name: finish-fritjoflammers-snakemake-methylanalysis-destrand_calls
description: Use this skill when orchestrating the retained "destrand_calls" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the destrand calls stage tied to upstream `extract_CpGs` and the downstream handoff to `methylkit_load`. It tracks completion via `results/finish/destrand_calls.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: destrand_calls
  step_name: destrand calls
---

# Scope
Use this skill only for the `destrand_calls` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `extract_CpGs`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/destrand_calls.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/destrand_calls.done`
- Representative outputs: `results/finish/destrand_calls.done`
- Execution targets: `destrand_calls`
- Downstream handoff: `methylkit_load`

## Guardrails
- Treat `results/finish/destrand_calls.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/destrand_calls.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `methylkit_load` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/destrand_calls.done` exists and `methylkit_load` can proceed without re-running destrand calls.
