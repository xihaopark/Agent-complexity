---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-salmon_index
description: Use this skill when orchestrating the retained "salmon_index" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the salmon index stage tied to upstream `spoof_t2g` and the downstream handoff to `salmon_alevin`. It tracks completion via `results/finish/salmon_index.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: salmon_index
  step_name: salmon index
---

# Scope
Use this skill only for the `salmon_index` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `spoof_t2g`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/salmon_index.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/salmon_index.done`
- Representative outputs: `results/finish/salmon_index.done`
- Execution targets: `salmon_index`
- Downstream handoff: `salmon_alevin`

## Guardrails
- Treat `results/finish/salmon_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/salmon_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `salmon_alevin` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/salmon_index.done` exists and `salmon_alevin` can proceed without re-running salmon index.
