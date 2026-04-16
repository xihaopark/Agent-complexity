---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-salmon_alevin
description: Use this skill when orchestrating the retained "salmon_alevin" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the salmon alevin stage tied to upstream `salmon_index` and the downstream handoff to `alevin_fry_preprocess`. It tracks completion via `results/finish/salmon_alevin.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: salmon_alevin
  step_name: salmon alevin
---

# Scope
Use this skill only for the `salmon_alevin` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `salmon_index`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/salmon_alevin.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/salmon_alevin.done`
- Representative outputs: `results/finish/salmon_alevin.done`
- Execution targets: `salmon_alevin`
- Downstream handoff: `alevin_fry_preprocess`

## Guardrails
- Treat `results/finish/salmon_alevin.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/salmon_alevin.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `alevin_fry_preprocess` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/salmon_alevin.done` exists and `alevin_fry_preprocess` can proceed without re-running salmon alevin.
