---
name: finish-epigen-fetch-ngs-env_export
description: Use this skill when orchestrating the retained "env_export" step of the epigen fetch_ngs finish finish workflow. It keeps the env export stage and the downstream handoff to `config_export`. It tracks completion via `results/finish/env_export.done`.
metadata:
  workflow_id: epigen-fetch_ngs-finish
  workflow_name: epigen fetch_ngs finish
  step_id: env_export
  step_name: env export
---

# Scope
Use this skill only for the `env_export` step in `epigen-fetch_ngs-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/epigen-fetch_ngs-finish/steps/env_export.smk`
- Config file: `finish/epigen-fetch_ngs-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/env_export.done`
- Representative outputs: `results/finish/env_export.done`
- Execution targets: `env_export`
- Downstream handoff: `config_export`

## Guardrails
- Treat `results/finish/env_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/env_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `config_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/env_export.done` exists and `config_export` can proceed without re-running env export.
