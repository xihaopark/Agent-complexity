# fritjoflammers-snakemake-methylanalysis-finish LLM Execution Spec

## Purpose

- Source repository: `fritjoflammers__snakemake-methylanalysis`
- Source snakefile: `../workflow_candidates/fritjoflammers__snakemake-methylanalysis/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `extract_CpGs`
2. `destrand_calls`
3. `methylkit_load`
4. `methylkit_filter_normalize`
5. `datavzrd_methylkit_filt_norm`
6. `methylkit_split`
7. `methylkit_unite_per_chr_all`
8. `methylkit_remove_variant_sites`
9. `methylkit_split_mku2tibble`
10. `datavzrd_methylkit_unite`
11. `methylkit_clustering`
12. `methylkit_pca`
13. `notebook_data_structure`
14. `gemma_subset_samples`
15. `macau_prep_counts_file`
16. `extract_column_from_spreadsheet`
17. `macau_prep_variables_file`
18. `macau_prep_covariate_file`
19. `macau_run`
20. `store_config`
21. `DSS_dmrs`
22. `all`
