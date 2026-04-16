# epigen-scrnaseq_processing_seurat-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__scrnaseq_processing_seurat`
- Source snakefile: `../workflow_candidates/epigen__scrnaseq_processing_seurat/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `prepare`
2. `merge`
3. `split`
4. `filter_cells`
5. `pseudobulk`
6. `save_counts`
7. `normalize`
8. `correct`
9. `metadata_plots`
10. `seurat_plots`
11. `env_export`
12. `config_export`
13. `annot_export`
14. `gene_list_export`
15. `all`
