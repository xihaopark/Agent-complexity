# joncahn-epigeneticbutton-finish LLM Execution Spec

## Purpose

- Source repository: `joncahn__epigeneticbutton`
- Source snakefile: `../workflow_candidates/joncahn__epigeneticbutton/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `map_only`
2. `coverage_chip`
3. `combined_analysis`
4. `prepare_reference`
5. `check_fasta`
6. `check_gff`
7. `check_gtf`
8. `check_chrom_sizes`
9. `prep_region_file`
10. `check_te_file`
11. `get_fastq_pe`
12. `get_fastq_se`
13. `run_fastqc`
14. `process_fastq_pe`
15. `process_fastq_se`
16. `get_available_bam`
17. `make_bt2_indices`
18. `bowtie2_map_pe`
19. `bowtie2_map_se`
20. `filter_chip_pe`
21. `filter_chip_se`
22. `make_chip_stats_pe`
23. `make_chip_stats_se`
24. `pe_or_se_chip_dispatch`
25. `make_coverage_chip`
26. `make_bigwig_chip`
27. `make_fingerprint_plot`
28. `calling_peaks_macs2_pe`
29. `calling_peaks_macs2_se`
30. `idr_analysis_replicates`
31. `merging_chip_replicates`
32. `making_pseudo_replicates`
33. `create_empty_file`
34. `best_peaks_pseudoreps`
35. `make_peak_stats`
36. `find_motifs_in_file`
37. `perform_pairwise_diff_peaks`
38. `all_chip`
39. `atac_shift_bam`
40. `atac_bam_to_bed`
41. `calling_peaks_atac`
42. `make_coverage_atac`
43. `all_atac`
44. `make_STAR_indices`
45. `STAR_map_pe`
46. `STAR_map_se`
47. `filter_rna_pe`
48. `filter_rna_se`
49. `make_rna_stats_pe`
50. `make_rna_stats_se`
51. `pe_or_se_rna_dispatch`
52. `merging_rna_replicates`
53. `make_rna_stranded_bigwigs`
54. `make_rna_unstranded_bigwigs`
55. `prep_files_for_DEGs`
56. `call_all_DEGs`
57. `gather_gene_expression_rpkm`
58. `plot_expression_levels`
59. `create_GO_database`
60. `perform_GO_on_target_file`
61. `call_rampage_TSS`
62. `all_rna`
63. `make_bismark_indices`
64. `bismark_map_pe`
65. `bismark_map_se`
66. `pe_or_se_mc_dispatch`
67. `make_mc_stats_pe`
68. `make_mc_stats_se`
69. `merging_mc_replicates`
70. `make_mc_bigwig_files`
71. `call_DMRs_pairwise`
72. `all_mc`
73. `download_modkit`
74. `get_dmc_input`
75. `dmc_input_checkpoint`
76. `prepare_modbam_for_pileup`
77. `modkit_pileup_dmc`
78. `copy_bedmethyl_input`
79. `merge_pileup_sources`
80. `modkit_summary_dmc`
81. `make_mc_stats_dmc`
82. `convert_bedmethyl_to_cx_report`
83. `deduplicate_srna_nextflexv3`
84. `make_bt2_indices_for_structural_RNAs`
85. `filter_structural_rna`
86. `dispatch_srna_fastq`
87. `make_bowtie1_indices`
88. `make_bowtie1_indices_large`
89. `shortstack_map`
90. `make_cluster_bedfiles`
91. `make_srna_size_stats`
92. `filter_size_srna_sample`
93. `merging_srna_replicates`
94. `make_srna_stranded_bigwigs`
95. `analyze_all_srna_samples_on_target_file`
96. `prep_files_for_differential_srna_clusters`
97. `call_all_differential_srna_clusters`
98. `all_srna`
99. `has_header`
100. `is_stranded`
101. `prepping_mapping_stats`
102. `plotting_mapping_stats`
103. `prepping_chip_peak_stats`
104. `plotting_peaks_stats_chip_tf`
105. `prepping_srna_sizes_stats`
106. `plotting_srna_sizes_stats`
107. `combine_clusterfiles`
108. `combine_peakfiles`
109. `combine_TSS`
110. `get_annotations_for_bedfile`
111. `plotting_upset_regions`
112. `making_stranded_matrix_on_targetfile`
113. `merging_matrix`
114. `computing_matrix_scales`
115. `plotting_heatmap_on_targetfile`
116. `sort_heatmap`
117. `plotting_sorted_heatmap_on_targetfile`
118. `plotting_profile_on_targetfile`
119. `prep_chromosomes_for_browser`
120. `prep_browser_on_region`
121. `make_single_loci_browser_plot`
122. `merge_region_browser_plots`
123. `summarize_tracks_pca`
124. `plot_PCA_correlation`
125. `all_combined`
126. `all`
