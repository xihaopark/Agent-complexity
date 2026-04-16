# akinyi-onyango-rna_seq_pipeline-finish LLM Execution Spec

## Purpose

- Source repository: `Akinyi-Onyango__rna_seq_pipeline`
- Source snakefile: `../workflow_candidates/Akinyi-Onyango__rna_seq_pipeline/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `quality_control`
2. `quality_filtering`
3. `qc_trimmed_files`
4. `generate_index`
5. `read_mapping`
6. `read_counts`
7. `differential_expression`
8. `all`
