---
name: finish-fritjoflammers-snakemake-methylanalysis-methylkit_split_mku2tibble
description: Use this skill when orchestrating the retained "methylkit_split_mku2tibble" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the methylkit split mku2tibble stage tied to upstream `methylkit_remove_variant_sites` and the downstream handoff to `datavzrd_methylkit_unite`. It tracks completion via `results/finish/methylkit_split_mku2tibble.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: methylkit_split_mku2tibble
  step_name: methylkit split mku2tibble
---

# Scope
Use this skill only for the `methylkit_split_mku2tibble` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `methylkit_remove_variant_sites`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/methylkit_split_mku2tibble.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/methylkit_split_mku2tibble.done`
- Representative outputs: `results/finish/methylkit_split_mku2tibble.done`
- Execution targets: `methylkit_split_mku2tibble`
- Downstream handoff: `datavzrd_methylkit_unite`

## Guardrails
- Treat `results/finish/methylkit_split_mku2tibble.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/methylkit_split_mku2tibble.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `datavzrd_methylkit_unite` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/methylkit_split_mku2tibble.done` exists and `datavzrd_methylkit_unite` can proceed without re-running methylkit split mku2tibble.
