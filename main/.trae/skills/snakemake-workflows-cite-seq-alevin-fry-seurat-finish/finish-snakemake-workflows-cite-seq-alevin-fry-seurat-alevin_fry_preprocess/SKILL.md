---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-alevin_fry_preprocess
description: Use this skill when orchestrating the retained "alevin_fry_preprocess" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the alevin fry preprocess stage tied to upstream `salmon_alevin` and the downstream handoff to `alevin_fry_quant`. It tracks completion via `results/finish/alevin_fry_preprocess.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: alevin_fry_preprocess
  step_name: alevin fry preprocess
---

# Scope
Use this skill only for the `alevin_fry_preprocess` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `salmon_alevin`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/alevin_fry_preprocess.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/alevin_fry_preprocess.done`
- Representative outputs: `results/finish/alevin_fry_preprocess.done`
- Execution targets: `alevin_fry_preprocess`
- Downstream handoff: `alevin_fry_quant`

## Guardrails
- Treat `results/finish/alevin_fry_preprocess.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/alevin_fry_preprocess.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `alevin_fry_quant` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/alevin_fry_preprocess.done` exists and `alevin_fry_quant` can proceed without re-running alevin fry preprocess.
