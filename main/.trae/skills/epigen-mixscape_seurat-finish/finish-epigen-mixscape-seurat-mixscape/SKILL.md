---
name: finish-epigen-mixscape-seurat-mixscape
description: Use this skill when orchestrating the retained "mixscape" step of the epigen mixscape_seurat finish finish workflow. It keeps the mixscape stage and the downstream handoff to `lda`. It tracks completion via `results/finish/mixscape.done`.
metadata:
  workflow_id: epigen-mixscape_seurat-finish
  workflow_name: epigen mixscape_seurat finish
  step_id: mixscape
  step_name: mixscape
---

# Scope
Use this skill only for the `mixscape` step in `epigen-mixscape_seurat-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/epigen-mixscape_seurat-finish/steps/mixscape.smk`
- Config file: `finish/epigen-mixscape_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/mixscape.done`
- Representative outputs: `results/finish/mixscape.done`
- Execution targets: `mixscape`
- Downstream handoff: `lda`

## Guardrails
- Treat `results/finish/mixscape.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/mixscape.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `lda` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/mixscape.done` exists and `lda` can proceed without re-running mixscape.
