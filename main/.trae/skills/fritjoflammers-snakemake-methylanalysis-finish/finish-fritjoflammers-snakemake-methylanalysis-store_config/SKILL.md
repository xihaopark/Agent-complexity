---
name: finish-fritjoflammers-snakemake-methylanalysis-store_config
description: Use this skill when orchestrating the retained "store_config" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the store config stage tied to upstream `macau_run` and the downstream handoff to `DSS_dmrs`. It tracks completion via `results/finish/store_config.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: store_config
  step_name: store config
---

# Scope
Use this skill only for the `store_config` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `macau_run`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/store_config.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/store_config.done`
- Representative outputs: `results/finish/store_config.done`
- Execution targets: `store_config`
- Downstream handoff: `DSS_dmrs`

## Guardrails
- Treat `results/finish/store_config.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/store_config.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `DSS_dmrs` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/store_config.done` exists and `DSS_dmrs` can proceed without re-running store config.
