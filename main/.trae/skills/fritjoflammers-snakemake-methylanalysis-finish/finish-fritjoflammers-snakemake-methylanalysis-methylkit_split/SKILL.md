---
name: finish-fritjoflammers-snakemake-methylanalysis-methylkit_split
description: Use this skill when orchestrating the retained "methylkit_split" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the methylkit split stage tied to upstream `datavzrd_methylkit_filt_norm` and the downstream handoff to `methylkit_unite_per_chr_all`. It tracks completion via `results/finish/methylkit_split.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: methylkit_split
  step_name: methylkit split
---

# Scope
Use this skill only for the `methylkit_split` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `datavzrd_methylkit_filt_norm`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/methylkit_split.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/methylkit_split.done`
- Representative outputs: `results/finish/methylkit_split.done`
- Execution targets: `methylkit_split`
- Downstream handoff: `methylkit_unite_per_chr_all`

## Guardrails
- Treat `results/finish/methylkit_split.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/methylkit_split.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `methylkit_unite_per_chr_all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/methylkit_split.done` exists and `methylkit_unite_per_chr_all` can proceed without re-running methylkit split.
