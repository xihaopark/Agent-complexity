---
name: finish-fritjoflammers-snakemake-methylanalysis-dss_dmrs
description: Use this skill when orchestrating the retained "DSS_dmrs" step of the fritjoflammers snakemake methylanalysis finish finish workflow. It keeps the DSS dmrs stage tied to upstream `store_config` and the downstream handoff to `all`. It tracks completion via `results/finish/DSS_dmrs.done`.
metadata:
  workflow_id: fritjoflammers-snakemake-methylanalysis-finish
  workflow_name: fritjoflammers snakemake methylanalysis finish
  step_id: DSS_dmrs
  step_name: DSS dmrs
---

# Scope
Use this skill only for the `DSS_dmrs` step in `fritjoflammers-snakemake-methylanalysis-finish`.

## Orchestration
- Upstream requirements: `store_config`
- Step file: `finish/fritjoflammers-snakemake-methylanalysis-finish/steps/DSS_dmrs.smk`
- Config file: `finish/fritjoflammers-snakemake-methylanalysis-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/DSS_dmrs.done`
- Representative outputs: `results/finish/DSS_dmrs.done`
- Execution targets: `DSS_dmrs`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/DSS_dmrs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/DSS_dmrs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/DSS_dmrs.done` exists and `all` can proceed without re-running DSS dmrs.
