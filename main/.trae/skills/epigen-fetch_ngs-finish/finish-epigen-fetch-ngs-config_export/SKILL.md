---
name: finish-epigen-fetch-ngs-config_export
description: Use this skill when orchestrating the retained "config_export" step of the epigen fetch_ngs finish finish workflow. It keeps the config export stage tied to upstream `env_export` and the downstream handoff to `iseq_download`. It tracks completion via `results/finish/config_export.done`.
metadata:
  workflow_id: epigen-fetch_ngs-finish
  workflow_name: epigen fetch_ngs finish
  step_id: config_export
  step_name: config export
---

# Scope
Use this skill only for the `config_export` step in `epigen-fetch_ngs-finish`.

## Orchestration
- Upstream requirements: `env_export`
- Step file: `finish/epigen-fetch_ngs-finish/steps/config_export.smk`
- Config file: `finish/epigen-fetch_ngs-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/config_export.done`
- Representative outputs: `results/finish/config_export.done`
- Execution targets: `config_export`
- Downstream handoff: `iseq_download`

## Guardrails
- Treat `results/finish/config_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/config_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `iseq_download` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/config_export.done` exists and `iseq_download` can proceed without re-running config export.
