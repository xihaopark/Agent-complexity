# single-cell-rna-seq-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__single-cell-rna-seq`
- Source snakefile: `../workflow_candidates/snakemake-workflows__single-cell-rna-seq/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `all_qc`
2. `load_counts`
3. `qc`
4. `explained_variance`
5. `gene_vs_gene`
6. `gene_tsne`
7. `filter_cells`
8. `cell_cycle`
9. `cell_cycle_scores`
10. `normalize`
11. `batch_effect_removal`
12. `hvg`
13. `correlation`
14. `hvg_pca`
15. `hvg_tsne`
16. `cellassign`
17. `plot_cellassign`
18. `celltype_tsne`
19. `plot_celltype_expressions`
20. `edger`
21. `plot_expression`
22. `all`
