# rna-longseq-de-isoform-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__rna-longseq-de-isoform`
- Source snakefile: `../workflow_candidates/snakemake-workflows__rna-longseq-de-isoform/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `sample_qa_plot`
2. `total_sample_qa_plot`
3. `alignment_qa`
4. `alignment_qa_report`
5. `bam_stats`
6. `download_ncbi_genome`
7. `download_ncbi_annotation`
8. `download_ensembl_genome`
9. `download_ensembl_annotation`
10. `get_genome`
11. `get_annotation`
12. `standardize_gff`
13. `genome_to_transcriptome`
14. `correct_transcriptome`
15. `filter_reads`
16. `build_minimap_index`
17. `map_reads`
18. `sam_to_bam`
19. `bam_sort`
20. `bam_index`
21. `count_reads`
22. `merge_read_counts`
23. `transcriptid_to_gene`
24. `deseq2_init`
25. `deseq2`
26. `pca`
27. `reads_manifest`
28. `gff_to_gtf`
29. `bam_to_bed`
30. `concatenate_beds`
31. `build_flair_genome_index`
32. `flair_align`
33. `flair_correct`
34. `flair_collapse`
35. `flair_quantify`
36. `flair_diffexp`
37. `flair_plot_isoforms`
38. `iso_analysis_report`
39. `get_indexed_protein_db`
40. `generate_gene_query`
41. `lambda_gene_annotation`
42. `get_protein_names`
43. `all`
