---
name: finish-fritjoflammers-snakemake-methylanalysis-methylkit_load
description: Use this skill when orchestrating the retained "methylkit_load" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the methylkit load stage tied to upstream `destrand_calls` and the downstream handoff to `methylkit_filter_normalize`. It tracks completion via `results/finish/methylkit_load.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: methylkit_load
  step_name: methylkit load
---

# Scope
Use this skill only for the `methylkit_load` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `destrand_calls`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/methylkit_load.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/methylkit_load.done`
- Representative outputs: `results/finish/methylkit_load.done`
- Execution targets: `methylkit_load`
- Downstream handoff: `methylkit_filter_normalize`

## Guardrails
- Treat `results/finish/methylkit_load.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/methylkit_load.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `methylkit_filter_normalize` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/methylkit_load.done` exists and `methylkit_filter_normalize` can proceed without re-running methylkit load.
