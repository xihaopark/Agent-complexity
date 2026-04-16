# chipseq-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__chipseq`
- Source snakefile: `../workflow_candidates/snakemake-workflows__chipseq/workflow/Snakefile`
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
3. `sra_get_fastq_pe`
4. `sra_get_fastq_se`
5. `gtf2bed`
6. `genome_faidx`
7. `bwa_index`
8. `chromosome_size`
9. `generate_igenomes`
10. `generate_igenomes_blacklist`
11. `bedtools_sort_blacklist`
12. `bedtools_complement_blacklist`
13. `get_gsize`
14. `fastqc`
15. `multiqc`
16. `cutadapt_pe`
17. `cutadapt_se`
18. `bwa_mem`
19. `merge_bams`
20. `mark_merged_duplicates`
21. `samtools_view_filter`
22. `bamtools_filter_json`
23. `samtools_sort`
24. `orphan_remove`
25. `samtools_sort_pe`
26. `merge_se_pe`
27. `samtools_flagstat`
28. `samtools_idxstats`
29. `samtools_stats`
30. `samtools_index`
31. `preseq_lc_extrap`
32. `collect_multiple_metrics`
33. `genomecov`
34. `sort_genomecov`
35. `bedGraphToBigWig`
36. `create_igv_bigwig`
37. `compute_matrix`
38. `plot_profile`
39. `plot_heatmap`
40. `phantompeakqualtools`
41. `phantompeak_correlation`
42. `phantompeak_multiqc`
43. `plot_fingerprint`
44. `macs2_callpeak_broad`
45. `macs2_callpeak_narrow`
46. `peaks_count`
47. `sm_report_peaks_count_plot`
48. `bedtools_intersect`
49. `frip_score`
50. `sm_rep_frip_score`
51. `create_igv_peaks`
52. `homer_annotatepeaks`
53. `plot_macs_qc`
54. `plot_homer_annotatepeaks`
55. `plot_sum_annotatepeaks`
56. `bedtools_merge_broad`
57. `bedtools_merge_narrow`
58. `macs2_merged_expand`
59. `create_consensus_bed`
60. `create_consensus_saf`
61. `plot_peak_intersect`
62. `create_consensus_igv`
63. `homer_consensus_annotatepeaks`
64. `trim_homer_consensus_annotatepeaks`
65. `merge_bool_and_annotatepeaks`
66. `feature_counts`
67. `featurecounts_modified_colnames`
68. `featurecounts_deseq2`
69. `create_deseq2_igv`
70. `all`
