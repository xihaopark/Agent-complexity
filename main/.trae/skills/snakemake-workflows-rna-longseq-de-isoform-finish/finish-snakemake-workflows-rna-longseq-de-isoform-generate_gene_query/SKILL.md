---
name: finish-snakemake-workflows-rna-longseq-de-isoform-generate_gene_query
description: Use this skill when orchestrating the retained "generate_gene_query" step of the snakemake workflows rna longseq de isoform finish finish workflow. It keeps the generate gene query stage tied to upstream `get_indexed_protein_db` and the downstream handoff to `lambda_gene_annotation`. It tracks completion via `results/finish/generate_gene_query.done`.
metadata:
  workflow_id: rna-longseq-de-isoform-finish
  workflow_name: snakemake workflows rna longseq de isoform finish
  step_id: generate_gene_query
  step_name: generate gene query
---

# Scope
Use this skill only for the `generate_gene_query` step in `rna-longseq-de-isoform-finish`.

## Orchestration
- Upstream requirements: `get_indexed_protein_db`
- Step file: `finish/rna-longseq-de-isoform-finish/steps/generate_gene_query.smk`
- Config file: `finish/rna-longseq-de-isoform-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/generate_gene_query.done`
- Representative outputs: `results/finish/generate_gene_query.done`
- Execution targets: `generate_gene_query`
- Downstream handoff: `lambda_gene_annotation`

## Guardrails
- Treat `results/finish/generate_gene_query.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/generate_gene_query.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `lambda_gene_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/generate_gene_query.done` exists and `lambda_gene_annotation` can proceed without re-running generate gene query.
