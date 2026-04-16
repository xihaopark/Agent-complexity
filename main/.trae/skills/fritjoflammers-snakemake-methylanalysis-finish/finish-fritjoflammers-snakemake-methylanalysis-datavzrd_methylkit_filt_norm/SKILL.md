---
name: finish-fritjoflammers-snakemake-methylanalysis-datavzrd_methylkit_filt_norm
description: Use this skill when orchestrating the retained "datavzrd_methylkit_filt_norm" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the datavzrd methylkit filt norm stage tied to upstream `methylkit_filter_normalize` and the downstream handoff to `methylkit_split`. It tracks completion via `results/finish/datavzrd_methylkit_filt_norm.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: datavzrd_methylkit_filt_norm
  step_name: datavzrd methylkit filt norm
---

# Scope
Use this skill only for the `datavzrd_methylkit_filt_norm` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `methylkit_filter_normalize`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/datavzrd_methylkit_filt_norm.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/datavzrd_methylkit_filt_norm.done`
- Representative outputs: `results/finish/datavzrd_methylkit_filt_norm.done`
- Execution targets: `datavzrd_methylkit_filt_norm`
- Downstream handoff: `methylkit_split`

## Guardrails
- Treat `results/finish/datavzrd_methylkit_filt_norm.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/datavzrd_methylkit_filt_norm.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `methylkit_split` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/datavzrd_methylkit_filt_norm.done` exists and `methylkit_split` can proceed without re-running datavzrd methylkit filt norm.
