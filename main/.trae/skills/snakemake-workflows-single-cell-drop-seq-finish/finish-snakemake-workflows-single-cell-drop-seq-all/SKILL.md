---
name: finish-snakemake-workflows-single-cell-drop-seq-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the all stage tied to upstream `create_publication_text`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `create_publication_text`
- Step file: `finish/single-cell-drop-seq-finish/steps/all.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
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
