# epigen-dea_seurat-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__dea_seurat`
- Source snakefile: `../workflow_candidates/epigen__dea_seurat/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `dea`
2. `aggregate`
3. `feature_lists`
4. `volcanos`
5. `heatmap`
6. `env_export`
7. `config_export`
8. `annot_export`
9. `feature_list_export`
10. `all`
