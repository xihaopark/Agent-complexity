---
name: finish-epigen-mixscape-seurat-lda
description: Use this skill when orchestrating the retained "lda" step of the epigen mixscape_seurat finish finish workflow. It keeps the lda stage tied to upstream `mixscape` and the downstream handoff to `visualize`. It tracks completion via `results/finish/lda.done`.
metadata:
  workflow_id: epigen-mixscape_seurat-finish
  workflow_name: epigen mixscape_seurat finish
  step_id: lda
  step_name: lda
---

# Scope
Use this skill only for the `lda` step in `epigen-mixscape_seurat-finish`.

## Orchestration
- Upstream requirements: `mixscape`
- Step file: `finish/epigen-mixscape_seurat-finish/steps/lda.smk`
- Config file: `finish/epigen-mixscape_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/lda.done`
- Representative outputs: `results/finish/lda.done`
- Execution targets: `lda`
- Downstream handoff: `visualize`

## Guardrails
- Treat `results/finish/lda.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/lda.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `visualize` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/lda.done` exists and `visualize` can proceed without re-running lda.
