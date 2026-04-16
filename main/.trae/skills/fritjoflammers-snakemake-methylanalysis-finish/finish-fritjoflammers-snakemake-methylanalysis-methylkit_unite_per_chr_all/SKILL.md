---
name: finish-fritjoflammers-snakemake-methylanalysis-methylkit_unite_per_chr_all
description: Use this skill when orchestrating the retained "methylkit_unite_per_chr_all" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the methylkit unite per chr all stage tied to upstream `methylkit_split` and the downstream handoff to `methylkit_remove_variant_sites`. It tracks completion via `results/finish/methylkit_unite_per_chr_all.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: methylkit_unite_per_chr_all
  step_name: methylkit unite per chr all
---

# Scope
Use this skill only for the `methylkit_unite_per_chr_all` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `methylkit_split`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/methylkit_unite_per_chr_all.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/methylkit_unite_per_chr_all.done`
- Representative outputs: `results/finish/methylkit_unite_per_chr_all.done`
- Execution targets: `methylkit_unite_per_chr_all`
- Downstream handoff: `methylkit_remove_variant_sites`

## Guardrails
- Treat `results/finish/methylkit_unite_per_chr_all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/methylkit_unite_per_chr_all.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `methylkit_remove_variant_sites` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/methylkit_unite_per_chr_all.done` exists and `methylkit_remove_variant_sites` can proceed without re-running methylkit unite per chr all.
