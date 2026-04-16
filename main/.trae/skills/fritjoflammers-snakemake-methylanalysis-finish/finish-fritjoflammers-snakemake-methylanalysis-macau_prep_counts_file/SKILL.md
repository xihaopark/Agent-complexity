---
name: finish-fritjoflammers-snakemake-methylanalysis-macau_prep_counts_file
description: Use this skill when orchestrating the retained "macau_prep_counts_file" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the macau prep counts file stage tied to upstream `gemma_subset_samples` and the downstream handoff to `extract_column_from_spreadsheet`. It tracks completion via `results/finish/macau_prep_counts_file.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: macau_prep_counts_file
  step_name: macau prep counts file
---

# Scope
Use this skill only for the `macau_prep_counts_file` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `gemma_subset_samples`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/macau_prep_counts_file.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/macau_prep_counts_file.done`
- Representative outputs: `results/finish/macau_prep_counts_file.done`
- Execution targets: `macau_prep_counts_file`
- Downstream handoff: `extract_column_from_spreadsheet`

## Guardrails
- Treat `results/finish/macau_prep_counts_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/macau_prep_counts_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract_column_from_spreadsheet` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/macau_prep_counts_file.done` exists and `extract_column_from_spreadsheet` can proceed without re-running macau prep counts file.
