---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-alevin_fry_quant
description: Use this skill when orchestrating the retained "alevin_fry_quant" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the alevin fry quant stage tied to upstream `alevin_fry_preprocess` and the downstream handoff to `seurat`. It tracks completion via `results/finish/alevin_fry_quant.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: alevin_fry_quant
  step_name: alevin fry quant
---

# Scope
Use this skill only for the `alevin_fry_quant` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `alevin_fry_preprocess`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/alevin_fry_quant.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/alevin_fry_quant.done`
- Representative outputs: `results/finish/alevin_fry_quant.done`
- Execution targets: `alevin_fry_quant`
- Downstream handoff: `seurat`

## Guardrails
- Treat `results/finish/alevin_fry_quant.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/alevin_fry_quant.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `seurat` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/alevin_fry_quant.done` exists and `seurat` can proceed without re-running alevin fry quant.
