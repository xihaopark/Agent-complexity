---
name: finish-snakemake-workflows-cellranger-multi-cellranger_multi_files_summaries
description: Use this skill when orchestrating the retained "cellranger_multi_files_summaries" step of the snakemake workflows cellranger multi finish finish workflow. It keeps the cellranger multi files summaries stage tied to upstream `cellranger_multi_run` and the downstream handoff to `cellranger_multi_files_multiplexing_global`. It tracks completion via `results/finish/cellranger_multi_files_summaries.done`.
metadata:
  workflow_id: cellranger-multi-finish
  workflow_name: snakemake workflows cellranger multi finish
  step_id: cellranger_multi_files_summaries
  step_name: cellranger multi files summaries
---

# Scope
Use this skill only for the `cellranger_multi_files_summaries` step in `cellranger-multi-finish`.

## Orchestration
- Upstream requirements: `cellranger_multi_run`
- Step file: `finish/cellranger-multi-finish/steps/cellranger_multi_files_summaries.smk`
- Config file: `finish/cellranger-multi-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cellranger_multi_files_summaries.done`
- Representative outputs: `results/finish/cellranger_multi_files_summaries.done`
- Execution targets: `cellranger_multi_files_summaries`
- Downstream handoff: `cellranger_multi_files_multiplexing_global`

## Guardrails
- Treat `results/finish/cellranger_multi_files_summaries.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cellranger_multi_files_summaries.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `cellranger_multi_files_multiplexing_global` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cellranger_multi_files_summaries.done` exists and `cellranger_multi_files_multiplexing_global` can proceed without re-running cellranger multi files summaries.
