---
name: finish-epigen-mixscape-seurat-all
description: Use this skill when orchestrating the retained "all" step of the epigen mixscape_seurat finish finish workflow. It keeps the all stage tied to upstream `annot_export`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: epigen-mixscape_seurat-finish
  workflow_name: epigen mixscape_seurat finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `epigen-mixscape_seurat-finish`.

## Orchestration
- Upstream requirements: `annot_export`
- Step file: `finish/epigen-mixscape_seurat-finish/steps/all.smk`
- Config file: `finish/epigen-mixscape_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
