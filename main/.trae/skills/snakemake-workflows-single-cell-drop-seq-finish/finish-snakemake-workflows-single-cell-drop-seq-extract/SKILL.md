---
name: finish-snakemake-workflows-single-cell-drop-seq-extract
description: Use this skill when orchestrating the retained "extract" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the extract stage tied to upstream `map` and the downstream handoff to `split_species`. It tracks completion via `results/finish/extract.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: extract
  step_name: extract
---

# Scope
Use this skill only for the `extract` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `map`
- Step file: `finish/single-cell-drop-seq-finish/steps/extract.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract.done`
- Representative outputs: `results/finish/extract.done`
- Execution targets: `extract`
- Downstream handoff: `split_species`

## Guardrails
- Treat `results/finish/extract.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `split_species` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract.done` exists and `split_species` can proceed without re-running extract.
