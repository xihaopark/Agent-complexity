# rna-seq-kallisto-sleuth-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__rna-seq-kallisto-sleuth`
- Source snakefile: `../workflow_candidates/snakemake-workflows__rna-seq-kallisto-sleuth/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `fastp_se`
2. `fastp_pe`
3. `max_read_length`
4. `get_aligned_pos`
5. `get_selected_transcripts_aligned_read_bins`
6. `get_selected_transcripts_sample_QC_histogram`
7. `get_sample_QC_histogram`
8. `get_transcriptome`
9. `get_annotation`
10. `get_transcript_info`
11. `get_pfam`
12. `convert_pfam`
13. `calculate_cpat_hexamers`
14. `calculate_cpat_logit_model`
15. `get_spia_db`
16. `cds_polyA_T_removal`
17. `get_main_transcripts_fasta`
18. `kallisto_long_index`
19. `kallisto_long_bus`
20. `bustools_sort`
21. `bustools_count`
22. `kallisto_long_quant_tcc`
23. `kallisto_index`
24. `kallisto_quant`
25. `bwa_index`
26. `bwa_mem`
27. `get_only_main_transcript_reads_closest_to_3_prime`
28. `get_main_transcript_fastq`
29. `kallisto_3prime_index`
30. `kallisto_3prime_quant`
31. `kallisto_samtools_sort`
32. `kallisto_samtools_index`
33. `compose_sample_sheet`
34. `sleuth_init`
35. `sleuth_diffexp`
36. `ihw_fdr_control`
37. `plot_bootstrap`
38. `prepare_pca`
39. `plot_pca`
40. `plot_diffexp_pval_hist`
41. `logcount_matrix`
42. `tpm_matrix`
43. `plot_diffexp_heatmap`
44. `plot_group_density`
45. `plot_scatter`
46. `plot_fragment_length_dist`
47. `plot_vars`
48. `vega_volcano_plot`
49. `init_isoform_switch`
50. `calculate_protein_domains`
51. `calculate_coding_potential`
52. `annotate_isoform_switch`
53. `spia`
54. `fgsea`
55. `fgsea_plot_gene_sets`
56. `ens_gene_to_go`
57. `download_go_obo`
58. `goatools_go_enrichment`
59. `postprocess_go_enrichment`
60. `postprocess_diffexp`
61. `postprocess_tpm_matrix`
62. `plot_enrichment_scatter`
63. `plot_pathway_scatter`
64. `spia_datavzrd`
65. `diffexp_datavzrd`
66. `go_enrichment_datavzrd`
67. `meta_compare_datavzrd`
68. `inputs_datavzrd`
69. `bam_paired_to_fastq`
70. `bam_single_to_fastq`
71. `meta_compare_diffexp`
72. `meta_compare_enrichment`
73. `meta_compare_pathways`
74. `all`
