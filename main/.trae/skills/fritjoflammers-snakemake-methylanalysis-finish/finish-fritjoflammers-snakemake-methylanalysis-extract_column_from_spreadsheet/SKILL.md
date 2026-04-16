---
name: finish-fritjoflammers-snakemake-methylanalysis-extract_column_from_spreadsheet
description: Use this skill when orchestrating the retained "extract_column_from_spreadsheet" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the extract column from spreadsheet stage tied to upstream `macau_prep_counts_file` and the downstream handoff to `macau_prep_variables_file`. It tracks completion via `results/finish/extract_column_from_spreadsheet.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: extract_column_from_spreadsheet
  step_name: extract column from spreadsheet
---

# Scope
Use this skill only for the `extract_column_from_spreadsheet` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `macau_prep_counts_file`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/extract_column_from_spreadsheet.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_column_from_spreadsheet.done`
- Representative outputs: `results/finish/extract_column_from_spreadsheet.done`
- Execution targets: `extract_column_from_spreadsheet`
- Downstream handoff: `macau_prep_variables_file`

## Guardrails
- Treat `results/finish/extract_column_from_spreadsheet.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_column_from_spreadsheet.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `macau_prep_variables_file` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_column_from_spreadsheet.done` exists and `macau_prep_variables_file` can proceed without re-running extract column from spreadsheet.
