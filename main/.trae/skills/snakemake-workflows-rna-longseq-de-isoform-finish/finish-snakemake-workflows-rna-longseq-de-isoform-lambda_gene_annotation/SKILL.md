---
name: finish-snakemake-workflows-rna-longseq-de-isoform-lambda_gene_annotation
description: Use this skill when orchestrating the retained "lambda_gene_annotation" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the lambda gene annotation stage tied to upstream `generate_gene_query` and the downstream handoff to `get_protein_names`. It tracks completion via `results/finish/lambda_gene_annotation.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: lambda_gene_annotation
  step_name: lambda gene annotation
---

# Scope
Use this skill only for the `lambda_gene_annotation` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `generate_gene_query`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/lambda_gene_annotation.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/lambda_gene_annotation.done`
- Representative outputs: `results/finish/lambda_gene_annotation.done`
- Execution targets: `lambda_gene_annotation`
- Downstream handoff: `get_protein_names`

## Guardrails
- Treat `results/finish/lambda_gene_annotation.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/lambda_gene_annotation.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_protein_names` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/lambda_gene_annotation.done` exists and `get_protein_names` can proceed without re-running lambda gene annotation.
