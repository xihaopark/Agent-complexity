---
name: finish-snakemake-workflows-single-cell-drop-seq-create_publication_text
description: Use this skill when orchestrating the retained "create_publication_text" step of the snakemake workflows single cell drop seq finish finish workflow. It keeps the create publication text stage tied to upstream `summary_stats` and the downstream handoff to `all`. It tracks completion via `results/finish/create_publication_text.done`.
metadata:
  workflow_id: single-cell-drop-seq-finish
  workflow_name: snakemake workflows single cell drop seq finish
  step_id: create_publication_text
  step_name: create publication text
---

# Scope
Use this skill only for the `create_publication_text` step in `single-cell-drop-seq-finish`.

## Orchestration
- Upstream requirements: `summary_stats`
- Step file: `finish/single-cell-drop-seq-finish/steps/create_publication_text.smk`
- Config file: `finish/single-cell-drop-seq-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/create_publication_text.done`
- Representative outputs: `results/finish/create_publication_text.done`
- Execution targets: `create_publication_text`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/create_publication_text.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/create_publication_text.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/create_publication_text.done` exists and `all` can proceed without re-running create publication text.
