# epigen-unsupervised_analysis-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__unsupervised_analysis`
- Source snakefile: `../workflow_candidates/epigen__unsupervised_analysis/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `aggregate_all_clustering_results`
2. `aggregate_clustering_results`
3. `aggregate_rank_internal`
4. `annot_export`
5. `clustree_analysis`
6. `clustree_analysis_metadata`
7. `config_export`
8. `densmap_embed`
9. `distance_matrix`
10. `env_export`
11. `leiden_cluster`
12. `pca`
13. `plot_dimred_clustering`
14. `plot_dimred_features`
15. `plot_dimred_interactive`
16. `plot_dimred_metadata`
17. `plot_heatmap`
18. `plot_indices`
19. `plot_pca_diagnostics`
20. `plot_umap_connectivity`
21. `plot_umap_diagnostics`
22. `prep_feature_plot`
23. `umap_embed`
24. `umap_graph`
25. `validation_external`
26. `validation_internal`
27. `all`
