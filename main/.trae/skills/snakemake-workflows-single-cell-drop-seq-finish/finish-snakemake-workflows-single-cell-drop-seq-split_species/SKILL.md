---
name: finish-snakemake-workflows-single-cell-drop-seq-split_species
description: Use this skill when orchestrating the retained "split_species" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the split species stage tied to upstream `extract` and the downstream handoff to `extract_species`. It tracks completion via `results/finish/split_species.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: split_species
  step_name: split species
---

# Scope
Use this skill only for the `split_species` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `extract`
- Step file: `finish/single-cell-drop-seq-finish/steps/split_species.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/split_species.done`
- Representative outputs: `results/finish/split_species.done`
- Execution targets: `split_species`
- Downstream handoff: `extract_species`

## Guardrails
- Treat `results/finish/split_species.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/split_species.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `extract_species` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/split_species.done` exists and `extract_species` can proceed without re-running split species.
