---
name: finish-snakemake-workflows-cite-seq-alevin-fry-seurat-seurat
description: Use this skill when orchestrating the retained "seurat" step of the snakemake workflows cite seq alevin fry seurat finish finish workflow. It keeps the seurat stage tied to upstream `alevin_fry_quant` and the downstream handoff to `plot_initial_hto_counts`. It tracks completion via `results/finish/seurat.done`.
metadata:
  workflow_id: cite-seq-alevin-fry-seurat-finish
  workflow_name: snakemake workflows cite seq alevin fry seurat finish
  step_id: seurat
  step_name: seurat
---

# Scope
Use this skill only for the `seurat` step in `cite-seq-alevin-fry-seurat-finish`.

## Orchestration
- Upstream requirements: `alevin_fry_quant`
- Step file: `finish/cite-seq-alevin-fry-seurat-finish/steps/seurat.smk`
- Config file: `finish/cite-seq-alevin-fry-seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/seurat.done`
- Representative outputs: `results/finish/seurat.done`
- Execution targets: `seurat`
- Downstream handoff: `plot_initial_hto_counts`

## Guardrails
- Treat `results/finish/seurat.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/seurat.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `plot_initial_hto_counts` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/seurat.done` exists and `plot_initial_hto_counts` can proceed without re-running seurat.
