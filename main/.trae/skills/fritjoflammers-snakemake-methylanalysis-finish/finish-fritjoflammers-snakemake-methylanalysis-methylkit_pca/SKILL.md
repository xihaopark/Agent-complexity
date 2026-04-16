---
name: finish-fritjoflammers-snakemake-methylanalysis-methylkit_pca
description: Use this skill when orchestrating the retained "methylkit_pca" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the methylkit pca stage tied to upstream `methylkit_clustering` and the downstream handoff to `notebook_data_structure`. It tracks completion via `results/finish/methylkit_pca.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: methylkit_pca
  step_name: methylkit pca
---

# Scope
Use this skill only for the `methylkit_pca` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `methylkit_clustering`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/methylkit_pca.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/methylkit_pca.done`
- Representative outputs: `results/finish/methylkit_pca.done`
- Execution targets: `methylkit_pca`
- Downstream handoff: `notebook_data_structure`

## Guardrails
- Treat `results/finish/methylkit_pca.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/methylkit_pca.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `notebook_data_structure` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/methylkit_pca.done` exists and `notebook_data_structure` can proceed without re-running methylkit pca.
