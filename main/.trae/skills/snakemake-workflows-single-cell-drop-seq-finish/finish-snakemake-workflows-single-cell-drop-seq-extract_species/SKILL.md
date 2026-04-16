---
name: finish-snakemake-workflows-single-cell-drop-seq-extract_species
description: Use this skill when orchestrating the retained "extract_species" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the extract species stage tied to upstream `split_species` and the downstream handoff to `merge`. It tracks completion via `results/finish/extract_species.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: extract_species
  step_name: extract species
---

# Scope
Use this skill only for the `extract_species` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `split_species`
- Step file: `finish/single-cell-drop-seq-finish/steps/extract_species.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/extract_species.done`
- Representative outputs: `results/finish/extract_species.done`
- Execution targets: `extract_species`
- Downstream handoff: `merge`

## Guardrails
- Treat `results/finish/extract_species.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/extract_species.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/extract_species.done` exists and `merge` can proceed without re-running extract species.
