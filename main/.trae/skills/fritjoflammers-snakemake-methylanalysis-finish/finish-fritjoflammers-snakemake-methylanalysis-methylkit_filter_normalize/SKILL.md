---
name: finish-fritjoflammers-snakemake-methylanalysis-methylkit_filter_normalize
description: Use this skill when orchestrating the retained "methylkit_filter_normalize" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the methylkit filter normalize stage tied to upstream `methylkit_load` and the downstream handoff to `datavzrd_methylkit_filt_norm`. It tracks completion via `results/finish/methylkit_filter_normalize.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: methylkit_filter_normalize
  step_name: methylkit filter normalize
---

# Scope
Use this skill only for the `methylkit_filter_normalize` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `methylkit_load`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/methylkit_filter_normalize.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/methylkit_filter_normalize.done`
- Representative outputs: `results/finish/methylkit_filter_normalize.done`
- Execution targets: `methylkit_filter_normalize`
- Downstream handoff: `datavzrd_methylkit_filt_norm`

## Guardrails
- Treat `results/finish/methylkit_filter_normalize.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/methylkit_filter_normalize.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `datavzrd_methylkit_filt_norm` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/methylkit_filter_normalize.done` exists and `datavzrd_methylkit_filt_norm` can proceed without re-running methylkit filter normalize.
