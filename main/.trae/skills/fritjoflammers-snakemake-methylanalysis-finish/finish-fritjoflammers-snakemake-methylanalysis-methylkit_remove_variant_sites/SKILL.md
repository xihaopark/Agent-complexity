---
name: finish-fritjoflammers-snakemake-methylanalysis-methylkit_remove_variant_sites
description: Use this skill when orchestrating the retained "methylkit_remove_variant_sites" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the methylkit remove variant sites stage tied to upstream `methylkit_unite_per_chr_all` and the downstream handoff to `methylkit_split_mku2tibble`. It tracks completion via `results/finish/methylkit_remove_variant_sites.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: methylkit_remove_variant_sites
  step_name: methylkit remove variant sites
---

# Scope
Use this skill only for the `methylkit_remove_variant_sites` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `methylkit_unite_per_chr_all`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/methylkit_remove_variant_sites.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/methylkit_remove_variant_sites.done`
- Representative outputs: `results/finish/methylkit_remove_variant_sites.done`
- Execution targets: `methylkit_remove_variant_sites`
- Downstream handoff: `methylkit_split_mku2tibble`

## Guardrails
- Treat `results/finish/methylkit_remove_variant_sites.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/methylkit_remove_variant_sites.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `methylkit_split_mku2tibble` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/methylkit_remove_variant_sites.done` exists and `methylkit_split_mku2tibble` can proceed without re-running methylkit remove variant sites.
