# epigen-mixscape_seurat-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__mixscape_seurat`
- Source snakefile: `../workflow_candidates/epigen__mixscape_seurat/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `mixscape`
2. `lda`
3. `visualize`
4. `env_export`
5. `config_export`
6. `annot_export`
7. `all`
