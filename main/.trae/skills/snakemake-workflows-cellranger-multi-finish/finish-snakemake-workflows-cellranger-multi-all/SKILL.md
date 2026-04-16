---
name: finish-snakemake-workflows-cellranger-multi-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows cellranger multi finish finish workflow. It keeps the all stage tied to upstream `cellranger_multi_files_vdj_per_sample`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: cellranger-multi-finish
  workflow_name: snakemake workflows cellranger multi finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `cellranger-multi-finish`.

## Orchestration
- Upstream requirements: `cellranger_multi_files_vdj_per_sample`
- Step file: `finish/cellranger-multi-finish/steps/all.smk`
- Config file: `finish/cellranger-multi-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/all.done`
- Representative outputs: `results/finish/all.done`
- Execution targets: `all`
- Downstream handoff: none

## Guardrails
- Treat `results/finish/all.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/all.smk` so the step remains separable and replayable inside the finish workflow.

## Done Criteria
Mark this step complete only when `results/finish/all.done` exists and matches the intended step boundary.
