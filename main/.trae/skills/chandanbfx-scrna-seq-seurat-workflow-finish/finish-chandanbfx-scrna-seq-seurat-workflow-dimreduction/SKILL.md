---
name: finish-chandanbfx-scrna-seq-seurat-workflow-dimreduction
description: Use this skill when orchestrating the retained "dimreduction" step of the chandanbfx scrna seq seurat workflow finish finish workflow. It keeps the dimreduction stage tied to upstream `batch_correction` and the downstream handoff to `clustering`. It tracks completion via `results/finish/dimreduction.done`.
metadata:
  workflow_id: chandanbfx-scrna-seq-seurat-workflow-finish
  workflow_name: chandanbfx scrna seq seurat workflow finish
  step_id: dimreduction
  step_name: dimreduction
---

# Scope
Use this skill only for the `dimreduction` step in `chandanbfx-scrna-seq-seurat-workflow-finish`.

## Orchestration
- Upstream requirements: `batch_correction`
- Step file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/steps/dimreduction.smk`
- Config file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/dimreduction.done`
- Representative outputs: `results/finish/dimreduction.done`
- Execution targets: `dimreduction`
- Downstream handoff: `clustering`

## Guardrails
- Treat `results/finish/dimreduction.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/dimreduction.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `clustering` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/dimreduction.done` exists and `clustering` can proceed without re-running dimreduction.
