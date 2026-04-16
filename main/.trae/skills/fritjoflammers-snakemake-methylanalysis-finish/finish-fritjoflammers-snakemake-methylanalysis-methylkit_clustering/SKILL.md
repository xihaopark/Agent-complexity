---
name: finish-fritjoflammers-snakemake-methylanalysis-methylkit_clustering
description: Use this skill when orchestrating the retained "methylkit_clustering" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the methylkit clustering stage tied to upstream `datavzrd_methylkit_unite` and the downstream handoff to `methylkit_pca`. It tracks completion via `results/finish/methylkit_clustering.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: methylkit_clustering
  step_name: methylkit clustering
---

# Scope
Use this skill only for the `methylkit_clustering` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `datavzrd_methylkit_unite`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/methylkit_clustering.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/methylkit_clustering.done`
- Representative outputs: `results/finish/methylkit_clustering.done`
- Execution targets: `methylkit_clustering`
- Downstream handoff: `methylkit_pca`

## Guardrails
- Treat `results/finish/methylkit_clustering.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/methylkit_clustering.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `methylkit_pca` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/methylkit_clustering.done` exists and `methylkit_pca` can proceed without re-running methylkit clustering.
