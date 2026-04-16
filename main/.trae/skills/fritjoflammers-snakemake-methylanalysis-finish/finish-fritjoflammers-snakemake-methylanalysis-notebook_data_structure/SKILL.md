---
name: finish-fritjoflammers-snakemake-methylanalysis-notebook_data_structure
description: Use this skill when orchestrating the retained "notebook_data_structure" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the notebook data structure stage tied to upstream `methylkit_pca` and the downstream handoff to `gemma_subset_samples`. It tracks completion via `results/finish/notebook_data_structure.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: notebook_data_structure
  step_name: notebook data structure
---

# Scope
Use this skill only for the `notebook_data_structure` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `methylkit_pca`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/notebook_data_structure.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/notebook_data_structure.done`
- Representative outputs: `results/finish/notebook_data_structure.done`
- Execution targets: `notebook_data_structure`
- Downstream handoff: `gemma_subset_samples`

## Guardrails
- Treat `results/finish/notebook_data_structure.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/notebook_data_structure.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gemma_subset_samples` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/notebook_data_structure.done` exists and `gemma_subset_samples` can proceed without re-running notebook data structure.
