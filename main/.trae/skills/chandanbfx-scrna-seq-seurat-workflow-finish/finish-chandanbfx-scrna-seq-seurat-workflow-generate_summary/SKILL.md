---
name: finish-chandanbfx-scrna-seq-seurat-workflow-generate_summary
description: Use this skill when orchestrating the retained "generate_summary" step of the chandanbfx scrna seq seurat workflow finish finish workflow. It keeps the generate summary stage tied to upstream `annotation` and the downstream handoff to `all`. It tracks completion via `results/finish/generate_summary.done`.
metadata:
  workflow_id: chandanbfx-scrna-seq-seurat-workflow-finish
  workflow_name: chandanbfx scrna seq seurat workflow finish
  step_id: generate_summary
  step_name: generate summary
---

# Scope
Use this skill only for the `generate_summary` step in `chandanbfx-scrna-seq-seurat-workflow-finish`.

## Orchestration
- Upstream requirements: `annotation`
- Step file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/steps/generate_summary.smk`
- Config file: `finish/chandanbfx-scrna-seq-seurat-workflow-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/generate_summary.done`
- Representative outputs: `results/finish/generate_summary.done`
- Execution targets: `generate_summary`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/generate_summary.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/generate_summary.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/generate_summary.done` exists and `all` can proceed without re-running generate summary.
