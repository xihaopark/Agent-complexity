---
name: finish-epigen-dea-limma-env_export
description: Use this skill when orchestrating the retained "env_export" step of the epigen dea_limma finish finish workflow. It keeps the env export stage tied to upstream `lfc_heatmap` and the downstream handoff to `config_export`. It tracks completion via `results/finish/env_export.done`.
metadata:
  workflow_id: epigen-dea_limma-finish
  workflow_name: epigen dea_limma finish
  step_id: env_export
  step_name: env export
---

# Scope
Use this skill only for the `env_export` step in `epigen-dea_limma-finish`.

## Orchestration
- Upstream requirements: `lfc_heatmap`
- Step file: `finish/epigen-dea_limma-finish/steps/env_export.smk`
- Config file: `finish/epigen-dea_limma-finish/config_basic/config.yaml`
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
