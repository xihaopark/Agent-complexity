# mckellardw-slide_snake-finish LLM Execution Spec

## Purpose

- Source repository: `mckellardw__slide_snake`
- Source snakefile: `../workflow_candidates/mckellardw__slide_snake/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `utils_index_BAM`
2. `BC_copy_barcode_map`
3. `BC_get_simple_whitelist`
4. `BC_write_whitelist_variants`
5. `ilmn_1a_merge_fastqs`
6. `ilmn_1b_cutadapt`
7. `ilmn_1b_cutadapt2`
8. `ilmn_1b_R1_hardTrimming`
9. `ilmn_1b_R1_internalTrimming`
10. `ilmn_1c_fastq_call_bc_from_adapter`
11. `ilmn_1c_filter_barcodes`
12. `ilmn_1c_tsv_bc_correction`
13. `ilmn_1c_summarize_bc_correction`
14. `ilmn_2a_extract_rRNA_fasta`
15. `ilmn_2a_build_rRNA_gtf`
16. `ilmn_2a_build_rRNA_bwa_index`
17. `ilmn_2a_bwa_rRNA_align`
18. `ilmn_2a_bwa_rRNA_get_no_rRNA_list`
19. `ilmn_2a_bwa_rRNA_filter_R1`
20. `ilmn_2a_bwa_rRNA_filter_trimmed_R1`
21. `ilmn_2a_bwa_rRNA_compress_unmapped`
22. `ilmn_2a_bwa_rRNA_filtered_fastqc`
23. `ilmn_2b_ribodetector`
24. `ilmn_2b_ribodetector_get_no_rRNA_list`
25. `ilmn_2b_ribodetector_filter_R1`
26. `ilmn_2b_ribodetector_filter_trimmed_R1`
27. `ilmn_2b_ribodetector_compress_fqs`
28. `ilmn_2c_qualimapQC_rRNA_bwa`
29. `ilmn_2c_qualimap_readqc_summary2csv_rRNA_bwa`
30. `ilmn_2c_qualimap_bamqc_rRNA_bwa`
31. `ilmn_2c_qualimap_bamqc_summary2csv_rRNA_bwa`
32. `ilmn_3a_STARsolo_firstPass`
33. `ilmn_3a_STARsolo_secondPass`
34. `ilmn_3a_compress_STAR_outs`
35. `ilmn_3a_cache_seurat_STAR`
36. `ilmn_3a_cache_h5ad_STAR`
37. `ilmn_3b_fastqc_unmapped`
38. `ilmn_3c_strand_split_bam`
39. `ilmn_3c_umitools_dedup_fwdBAM`
40. `ilmn_3c_umitools_dedup_revBAM`
41. `ilmn_3c_merge_dedup_bam`
42. `ilmn_3q_qualimapQC_STAR`
43. `ilmn_3q_qualimapQC_dedup_STAR`
44. `ilmn_3q_qualimap_rnaseq_summary2csv_STAR`
45. `ilmn_3q_qualimap_bamqc_STAR_raw`
46. `ilmn_3q_qualimap_bamqc_STAR_dedup`
47. `ilmn_3q_qualimap_bamqc_summary2csv_STAR`
48. `ilmn_3u_filter_noGN`
49. `ilmn_3u_calcHMMbed`
50. `ilmn_3u_filter_out_aTARs`
51. `ilmn_3u_bed_to_gtf`
52. `ilmn_3u_tagReads`
53. `ilmn_3u_sort_index_tagged_bam`
54. `ilmn_3u_extract_HMM_expression`
55. `ilmn_3u_counts_long2mtx`
56. `ilmn_3u_gzip_counts`
57. `ilmn_3u_plot_qc`
58. `ilmn_4a_kbpython_std`
59. `ilmn_4a_kbpython_std_remove_suffix`
60. `ilmn_4a_kbpython_std_compress_outs`
61. `ilmn_4a_cache_seurat_kbpython_std`
62. `ilmn_4a_cache_h5ad_kbpython_std`
63. `ilmn_5a_copy_R2_fq_for_mirge`
64. `ilmn_5a_miRge3_pseudobulk`
65. `ilmn_7a_fastQC_preTrim`
66. `ilmn_7a_fastQC_postTrim`
67. `ilmn_7a_fastQC_twiceTrim`
68. `ilmn_7b_readQC_0_rawInput`
69. `ilmn_7b_readQC_1_preCutadapt`
70. `ilmn_7b_readQC_2_postCutadapt`
71. `ilmn_7b_readQC_3_twiceCutadapt`
72. `ilmn_7b_readQC_3_bam`
73. `ilmn_7b_readQC_downsample`
74. `ilmn_7b_readQC_summaryplot`
75. `ilmn_7b_readQC_compress`
76. `ont_1a_merge_formats`
77. `ont_1a_call_adapter_scan`
78. `ont_1a_readIDs_by_adapter_type`
79. `ont_1a_adapter_scan_summary`
80. `ont_1a_merge_scan_lists`
81. `ont_1a_subset_fastq_by_adapter_type`
82. `ont_1a_compress_merged_fq`
83. `ont_1a_split_fastq_to_R1_R2`
84. `ont_1b_cutadapt`
85. `ont_1b_R1_hardTrimming`
86. `ont_1b_R1_internalTrim`
87. `ont_1b_cutadapt_internalTrimming`
88. `ont_1b_cutadapt_summary`
89. `ont_1c_fastq_call_bc_from_adapter`
90. `ont_1c_filter_barcodes`
91. `ont_1c_tsv_bc_correction`
92. `ont_1c_summarize_bc_correction`
93. `ont_2a_generate_junction_bed`
94. `ont_2a_align_minimap2_genome`
95. `ont_2a_sort_compress_output`
96. `ont_2a_add_corrected_barcodes`
97. `ont_2a_add_umis`
98. `ont_2a_filter_bam_empty_tags`
99. `ont_2a_featureCounts`
100. `ont_2a_add_featureCounts_to_bam`
101. `ont_2a_split_bam_by_strand`
102. `ont_2a_umitools_count`
103. `ont_2a_counts_to_sparse`
104. `ont_2a_cache_h5ad`
105. `ont_2a_cache_seurat`
106. `ont_2b_txome_align_minimap2_transcriptome`
107. `ont_2b_txome_add_corrected_barcodes`
108. `ont_2b_txome_add_umis`
109. `ont_2b_txome_filter_bam_empty_tags`
110. `ont_2b_txome_dedup_by_xb`
111. `ont_2b_txome_sort_by_xb`
112. `ont_2b_txome_oarfish_quant`
113. `ont_2b_txome_compress_oarfish_matrix`
114. `ont_2b_txome_cache_h5ad_minimap2`
115. `ont_2b_txome_cache_seurat_minimap2`
116. `ont_1f_sort_gtf`
117. `ont_2d_ultra_pipeline_genome`
118. `ont_2d_ultra_sort_compress_output`
119. `ont_2d_ultra_add_corrected_barcodes`
120. `ont_2d_ultra_add_umis`
121. `ont_2d_ultra_filter_bam_empty_tags`
122. `ont_2d_ultra_featureCounts`
123. `ont_2d_ultra_add_featureCounts_to_bam`
124. `ont_2d_ultra_umitools_count`
125. `ont_2d_ultra_counts_to_sparse`
126. `ont_2d_ultra_cache_h5ad`
127. `ont_2d_ultra_cache_seurat`
128. `ont_2e_isoquant`
129. `ont_2e_add_isoquant_genes_to_bam`
130. `ont_2e_add_isoquant_transcripts_to_bam`
131. `ont_2e_umitools_count`
132. `ont_2e_counts_to_sparse`
133. `ont_2e_cache_h5ad`
134. `ont_2e_cache_seurat`
135. `ont_3a_readQC_0_rawInput`
136. `ont_3a_readQC_1_preCutadapt`
137. `ont_3a_readQC_2_postCutadapt`
138. `ont_3a_readQC_3_bam`
139. `ont_3a_readQC_downsample`
140. `ont_3a_readQC_summaryplot`
141. `ont_3a_readQC_compress`
142. `ont_3b_qualimap`
143. `ont_3b_qualimap_readqc_summary2csv`
144. `ont_3b_qualimap_bamqc`
145. `ont_3b_qualimap_bamqc_summary2csv`
146. `all`
