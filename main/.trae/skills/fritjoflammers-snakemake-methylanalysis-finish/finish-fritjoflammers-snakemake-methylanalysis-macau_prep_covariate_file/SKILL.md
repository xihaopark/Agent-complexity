---
name: finish-fritjoflammers-snakemake-methylanalysis-macau_prep_covariate_file
description: Use this skill when orchestrating the retained "macau_prep_covariate_file" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the macau prep covariate file stage tied to upstream `macau_prep_variables_file` and the downstream handoff to `macau_run`. It tracks completion via `results/finish/macau_prep_covariate_file.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: macau_prep_covariate_file
  step_name: macau prep covariate file
---

# Scope
Use this skill only for the `macau_prep_covariate_file` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `macau_prep_variables_file`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/macau_prep_covariate_file.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/macau_prep_covariate_file.done`
- Representative outputs: `results/finish/macau_prep_covariate_file.done`
- Execution targets: `macau_prep_covariate_file`
- Downstream handoff: `macau_run`

## Guardrails
- Treat `results/finish/macau_prep_covariate_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/macau_prep_covariate_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `macau_run` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/macau_prep_covariate_file.done` exists and `macau_run` can proceed without re-running macau prep covariate file.
