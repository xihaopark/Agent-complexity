---
name: finish-epigen-dea-limma-volcanos
description: Use this skill when orchestrating the retained "volcanos" step of the epigen dea_limma finish finish workflow. It keeps the volcanos stage tied to upstream `fetch_file` and the downstream handoff to `lfc_heatmap`. It tracks completion via `results/finish/volcanos.done`.
metadata:
  workflow_id: epigen-dea_limma-finish
  workflow_name: epigen dea_limma finish
  step_id: volcanos
  step_name: volcanos
---

# Scope
Use this skill only for the `volcanos` step in `epigen-dea_limma-finish`.

## Orchestration
- Upstream requirements: `fetch_file`
- Step file: `finish/epigen-dea_limma-finish/steps/volcanos.smk`
- Config file: `finish/epigen-dea_limma-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/volcanos.done`
- Representative outputs: `results/finish/volcanos.done`
- Execution targets: `volcanos`
- Downstream handoff: `lfc_heatmap`

## Guardrails
- Treat `results/finish/volcanos.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/volcanos.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `lfc_heatmap` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/volcanos.done` exists and `lfc_heatmap` can proceed without re-running volcanos.
