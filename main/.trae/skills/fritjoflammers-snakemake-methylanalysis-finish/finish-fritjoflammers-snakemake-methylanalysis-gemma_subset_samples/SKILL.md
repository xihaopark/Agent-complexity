---
name: finish-fritjoflammers-snakemake-methylanalysis-gemma_subset_samples
description: Use this skill when orchestrating the retained "gemma_subset_samples" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the gemma subset samples stage tied to upstream `notebook_data_structure` and the downstream handoff to `macau_prep_counts_file`. It tracks completion via `results/finish/gemma_subset_samples.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: gemma_subset_samples
  step_name: gemma subset samples
---

# Scope
Use this skill only for the `gemma_subset_samples` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `notebook_data_structure`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/gemma_subset_samples.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gemma_subset_samples.done`
- Representative outputs: `results/finish/gemma_subset_samples.done`
- Execution targets: `gemma_subset_samples`
- Downstream handoff: `macau_prep_counts_file`

## Guardrails
- Treat `results/finish/gemma_subset_samples.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gemma_subset_samples.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `macau_prep_counts_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gemma_subset_samples.done` exists and `macau_prep_counts_file` can proceed without re-running gemma subset samples.
