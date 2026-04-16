# epigen-enrichment_analysis-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__enrichment_analysis`
- Source snakefile: `../workflow_candidates/epigen__enrichment_analysis/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `aggregate`
2. `annot_export`
3. `config_export`
4. `env_export`
5. `gene_ORA_GSEApy`
6. `gene_motif_enrichment_analysis_RcisTarget`
7. `gene_preranked_GSEApy`
8. `plot_enrichment_result`
9. `prepare_databases`
10. `process_results_pycisTarget`
11. `region_enrichment_analysis_GREAT`
12. `region_enrichment_analysis_LOLA`
13. `region_gene_association_GREAT`
14. `region_motif_enrichment_analysis_pycisTarget`
15. `visualize`
16. `all`
