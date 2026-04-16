---
name: finish-snakemake-workflows-cyrcular-calling-download_gene_annotation
description: Use this skill when orchestrating the retained "download_gene_annotation" step of the snakemake workflows cyrcular calling finish finish workflow. It keeps the download gene annotation stage tied to upstream `download_repeatmasker_annotation` and the downstream handoff to `minimap2_bam`. It tracks completion via `results/finish/download_gene_annotation.done`.
metadata:
  workflow_id: cyrcular-calling-finish
  workflow_name: snakemake workflows cyrcular calling finish
  step_id: download_gene_annotation
  step_name: download gene annotation
---

# Scope
Use this skill only for the `download_gene_annotation` step in `cyrcular-calling-finish`.

## Orchestration
- Upstream requirements: `download_repeatmasker_annotation`
- Step file: `finish/cyrcular-calling-finish/steps/download_gene_annotation.smk`
- Config file: `finish/cyrcular-calling-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/download_gene_annotation.done`
- Representative outputs: `results/finish/download_gene_annotation.done`
- Execution targets: `download_gene_annotation`
- Downstream handoff: `minimap2_bam`

## Guardrails
- Treat `results/finish/download_gene_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/download_gene_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `minimap2_bam` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/download_gene_annotation.done` exists and `minimap2_bam` can proceed without re-running download gene annotation.
