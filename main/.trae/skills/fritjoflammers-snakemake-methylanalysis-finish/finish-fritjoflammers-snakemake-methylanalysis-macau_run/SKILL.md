---
name: finish-fritjoflammers-snakemake-methylanalysis-macau_run
description: Use this skill when orchestrating the retained "macau_run" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the macau run stage tied to upstream `macau_prep_covariate_file` and the downstream handoff to `store_config`. It tracks completion via `results/finish/macau_run.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: macau_run
  step_name: macau run
---

# Scope
Use this skill only for the `macau_run` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `macau_prep_covariate_file`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/macau_run.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/macau_run.done`
- Representative outputs: `results/finish/macau_run.done`
- Execution targets: `macau_run`
- Downstream handoff: `store_config`

## Guardrails
- Treat `results/finish/macau_run.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/macau_run.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `store_config` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/macau_run.done` exists and `store_config` can proceed without re-running macau run.
