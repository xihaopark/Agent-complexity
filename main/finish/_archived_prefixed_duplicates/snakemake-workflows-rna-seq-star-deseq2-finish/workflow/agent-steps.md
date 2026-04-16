# rna-seq-star-deseq2-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__rna-seq-star-deseq2`
- Source snakefile: `../workflow_candidates/snakemake-workflows__rna-seq-star-deseq2/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `get_genome`
2. `get_annotation`
3. `genome_faidx`
4. `bwa_index`
5. `star_index`
6. `get_sra`
7. `fastp_se`
8. `fastp_pe`
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
19. `star_align`
20. `count_matrix`
21. `gene_2_symbol`
22. `deseq2_init`
23. `pca`
24. `deseq2`
25. `all`
