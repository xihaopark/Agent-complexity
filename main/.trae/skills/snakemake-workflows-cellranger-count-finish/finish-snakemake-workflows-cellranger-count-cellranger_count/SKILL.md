---
name: finish-snakemake-workflows-cellranger-count-cellranger_count
description: Use this skill when orchestrating the retained "cellranger_count" step of the snakemake workflows cellranger count finish finish workflow. It keeps the cellranger count stage tied to upstream `create_cellranger_library_csv` and the downstream handoff to `all`. It tracks completion via `results/finish/cellranger_count.done`.
metadata:
  workflow_id: cellranger-count-finish
  workflow_name: snakemake workflows cellranger count finish
  step_id: cellranger_count
  step_name: cellranger count
---

# Scope
Use this skill only for the `cellranger_count` step in `cellranger-count-finish`.

## Orchestration
- Upstream requirements: `create_cellranger_library_csv`
- Step file: `finish/cellranger-count-finish/steps/cellranger_count.smk`
- Config file: `finish/cellranger-count-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cellranger_count.done`
- Representative outputs: `results/finish/cellranger_count.done`
- Execution targets: `cellranger_count`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/cellranger_count.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cellranger_count.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cellranger_count.done` exists and `all` can proceed without re-running cellranger count.
