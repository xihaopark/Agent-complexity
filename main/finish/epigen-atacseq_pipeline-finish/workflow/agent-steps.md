# epigen-atacseq_pipeline-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__atacseq_pipeline`
- Source snakefile: `../workflow_candidates/epigen__atacseq_pipeline/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `env_export`
2. `config_export`
3. `annot_export`
4. `install_homer`
5. `align`
6. `tss_coverage`
7. `peak_calling`
8. `aggregate_stats`
9. `symlink_stats`
10. `multiqc`
11. `plot_sample_annotation`
12. `sample_annotation`
13. `get_promoter_regions`
14. `get_consensus_regions`
15. `quantify_support_sample`
16. `quantify_counts_sample`
17. `quantify_aggregate`
18. `homer_aggregate`
19. `map_consensus_tss`
20. `uropa_prepare`
21. `uropa_gencode`
22. `uropa_reg`
23. `homer_region_annotation`
24. `bedtools_annotation`
25. `region_annotation_aggregate`
26. `all`
