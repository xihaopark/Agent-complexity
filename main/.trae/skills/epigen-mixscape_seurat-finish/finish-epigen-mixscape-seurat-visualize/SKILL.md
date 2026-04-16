---
name: finish-epigen-mixscape-seurat-visualize
description: Use this skill when orchestrating the retained "visualize" step of the epigen mixscape_seurat finish finish workflow. It keeps the visualize stage tied to upstream `lda` and the downstream handoff to `env_export`. It tracks completion via `results/finish/visualize.done`.
metadata:
  workflow_id: epigen-mixscape_seurat-finish
  workflow_name: epigen mixscape_seurat finish
  step_id: visualize
  step_name: visualize
---

# Scope
Use this skill only for the `visualize` step in `epigen-mixscape_seurat-finish`.

## Orchestration
- Upstream requirements: `lda`
- Step file: `finish/epigen-mixscape_seurat-finish/steps/visualize.smk`
- Config file: `finish/epigen-mixscape_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/visualize.done`
- Representative outputs: `results/finish/visualize.done`
- Execution targets: `visualize`
- Downstream handoff: `env_export`

## Guardrails
- Treat `results/finish/visualize.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/visualize.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `env_export` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/visualize.done` exists and `env_export` can proceed without re-running visualize.
