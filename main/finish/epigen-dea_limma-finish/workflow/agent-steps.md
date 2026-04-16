# epigen-dea_limma-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__dea_limma`
- Source snakefile: `../workflow_candidates/epigen__dea_limma/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `dea`
2. `one_vs_all_contrasts`
3. `aggregate`
4. `ova_stats_plot`
5. `fetch_file`
6. `volcanos`
7. `lfc_heatmap`
8. `env_export`
9. `config_export`
10. `annot_export`
11. `feature_list_export`
12. `all`
