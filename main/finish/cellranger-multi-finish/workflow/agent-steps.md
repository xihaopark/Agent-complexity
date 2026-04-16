# cellranger-multi-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__cellranger-multi`
- Source snakefile: `../workflow_candidates/snakemake-workflows__cellranger-multi/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `follow_pedantic_cell_ranger_naming_scheme`
2. `create_cellranger_multi_config_csv`
3. `cellranger_multi_run`
4. `cellranger_multi_files_summaries`
5. `cellranger_multi_files_multiplexing_global`
6. `cellranger_multi_files_multiplexing_per_sample`
7. `cellranger_multi_files_multiplexing_antibody_global`
8. `cellranger_multi_files_multiplexing_crispr_global`
9. `cellranger_multi_files_gene_expression_global`
10. `cellranger_multi_files_gene_expression_per_sample`
11. `cellranger_multi_files_vdj_reference`
12. `cellranger_multi_files_vdj_global`
13. `cellranger_multi_files_vdj_per_sample`
14. `all`
