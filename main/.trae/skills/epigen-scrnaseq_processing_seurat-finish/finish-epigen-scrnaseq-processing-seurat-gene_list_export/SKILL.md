---
name: finish-epigen-scrnaseq-processing-seurat-gene_list_export
description: Use this skill when orchestrating the retained "gene_list_export" step of the epigen scrnaseq_processing_seurat finish finish workflow. It keeps the gene list export stage tied to upstream `annot_export` and the downstream handoff to `all`. It tracks completion via `results/finish/gene_list_export.done`.
metadata:
  workflow_id: epigen-scrnaseq_processing_seurat-finish
  workflow_name: epigen scrnaseq_processing_seurat finish
  step_id: gene_list_export
  step_name: gene list export
---

# Scope
Use this skill only for the `gene_list_export` step in `epigen-scrnaseq_processing_seurat-finish`.

## Orchestration
- Upstream requirements: `annot_export`
- Step file: `finish/epigen-scrnaseq_processing_seurat-finish/steps/gene_list_export.smk`
- Config file: `finish/epigen-scrnaseq_processing_seurat-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gene_list_export.done`
- Representative outputs: `results/finish/gene_list_export.done`
- Execution targets: `gene_list_export`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/gene_list_export.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gene_list_export.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gene_list_export.done` exists and `all` can proceed without re-running gene list export.
