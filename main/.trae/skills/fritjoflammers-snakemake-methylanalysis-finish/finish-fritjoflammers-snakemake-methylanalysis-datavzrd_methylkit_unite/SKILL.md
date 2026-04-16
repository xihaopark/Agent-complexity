---
name: finish-fritjoflammers-snakemake-methylanalysis-datavzrd_methylkit_unite
description: Use this skill when orchestrating the retained "datavzrd_methylkit_unite" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the datavzrd methylkit unite stage tied to upstream `methylkit_split_mku2tibble` and the downstream handoff to `methylkit_clustering`. It tracks completion via `results/finish/datavzrd_methylkit_unite.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: datavzrd_methylkit_unite
  step_name: datavzrd methylkit unite
---

# Scope
Use this skill only for the `datavzrd_methylkit_unite` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `methylkit_split_mku2tibble`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/datavzrd_methylkit_unite.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/datavzrd_methylkit_unite.done`
- Representative outputs: `results/finish/datavzrd_methylkit_unite.done`
- Execution targets: `datavzrd_methylkit_unite`
- Downstream handoff: `methylkit_clustering`

## Guardrails
- Treat `results/finish/datavzrd_methylkit_unite.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/datavzrd_methylkit_unite.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `methylkit_clustering` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/datavzrd_methylkit_unite.done` exists and `methylkit_clustering` can proceed without re-running datavzrd methylkit unite.
