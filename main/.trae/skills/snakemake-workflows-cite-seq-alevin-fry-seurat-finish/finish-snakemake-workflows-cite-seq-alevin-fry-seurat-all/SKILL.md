---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-all
description: Use this skill when orchestrating the retained "all" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the all stage tied to upstream `filter_to_singlets`. It tracks completion via `results/finish/all.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: all
  step_name: all
---

# Scope
Use this skill only for the `all` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `filter_to_singlets`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/all.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
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
