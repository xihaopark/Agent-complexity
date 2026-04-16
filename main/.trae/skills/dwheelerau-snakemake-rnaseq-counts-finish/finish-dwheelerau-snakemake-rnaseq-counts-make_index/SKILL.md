---
name: finish-dwheelerau-snakemake-rnaseq-counts-make_index
description: Use this skill when orchestrating the retained "make_index" step of the dwheelerau snakemake rnaseq counts finish finish workflow. It keeps the make index stage tied to upstream `project_setup` and the downstream handoff to `qc_trim`. It tracks completion via `results/finish/make_index.done`.
metadata:
  workflow_id: dwheelerau-snakemake-rnaseq-counts-finish
  workflow_name: dwheelerau snakemake rnaseq counts finish
  step_id: make_index
  step_name: make index
---

# Scope
Use this skill only for the `make_index` step in `dwheelerau-snakemake-rnaseq-counts-finish`.

## Orchestration
- Upstream requirements: `project_setup`
- Step file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/steps/make_index.smk`
- Config file: `finish/dwheelerau-snakemake-rnaseq-counts-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_index.done`
- Representative outputs: `results/finish/make_index.done`
- Execution targets: `make_index`
- Downstream handoff: `qc_trim`

## Guardrails
- Treat `results/finish/make_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `qc_trim` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_index.done` exists and `qc_trim` can proceed without re-running make index.
