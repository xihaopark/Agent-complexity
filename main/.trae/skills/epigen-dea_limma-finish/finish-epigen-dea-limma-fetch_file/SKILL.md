---
name: finish-epigen-dea-limma-fetch_file
description: Use this skill when orchestrating the retained "fetch_file" step of the epigen dea_limma finish finish workflow. It keeps the fetch file stage tied to upstream `ova_stats_plot` and the downstream handoff to `volcanos`. It tracks completion via `results/finish/fetch_file.done`.
metadata:
  workflow_id: epigen-dea_limma-finish
  workflow_name: epigen dea_limma finish
  step_id: fetch_file
  step_name: fetch file
---

# Scope
Use this skill only for the `fetch_file` step in `epigen-dea_limma-finish`.

## Orchestration
- Upstream requirements: `ova_stats_plot`
- Step file: `finish/epigen-dea_limma-finish/steps/fetch_file.smk`
- Config file: `finish/epigen-dea_limma-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/fetch_file.done`
- Representative outputs: `results/finish/fetch_file.done`
- Execution targets: `fetch_file`
- Downstream handoff: `volcanos`

## Guardrails
- Treat `results/finish/fetch_file.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/fetch_file.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `volcanos` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/fetch_file.done` exists and `volcanos` can proceed without re-running fetch file.
