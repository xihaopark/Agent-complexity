# epigen-rnaseq_pipeline-finish LLM Execution Spec

## Purpose

- Source repository: `epigen__rnaseq_pipeline`
- Source snakefile: `../workflow_candidates/epigen__rnaseq_pipeline/workflow/Snakefile`
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
4. `get_genome`
5. `get_annotation`
6. `genome_faidx`
7. `bwa_index`
8. `star_index`
9. `rseqc_gtf2bed`
10. `rseqc_junction_annotation`
11. `rseqc_junction_saturation`
12. `rseqc_stat`
13. `rseqc_infer`
14. `rseqc_innerdis`
15. `rseqc_readdis`
16. `rseqc_readdup`
17. `rseqc_readgc`
18. `multiqc`
19. `plot_sample_annotation`
20. `check_read_type`
21. `trim_filter`
22. `align`
23. `count_matrix`
24. `annotate_genes`
25. `sample_annotation`
26. `all`
