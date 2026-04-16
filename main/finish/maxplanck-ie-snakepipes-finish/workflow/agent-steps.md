# maxplanck-ie-snakepipes-finish LLM Execution Spec

## Purpose

- Source repository: `maxplanck-ie__snakePipes`
- Source snakefile: `../workflow_candidates/maxplanck-ie__snakePipes/snakePipes/workflows/ATACseq/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `link_bam`
2. `samtools_index_external`
3. `link_bam_bai_external`
4. `sambamba_flagstat`
5. `bamCoverage`
6. `bamCoverage_filtered`
7. `plotCoverage`
8. `multiBamSummary`
9. `plotCorrelation_pearson`
10. `plotCorrelation_spearman`
11. `plotPCA`
12. `estimate_read_filtering`
13. `computeGCBias`
14. `bamPE_fragment_size`
15. `bamcoverage_short_cleaned`
16. `multiQC`
17. `filterFragments`
18. `filterCoveragePerScaffolds`
19. `callOpenChromatin`
20. `tempChromSizes`
21. `HMMRATAC_peaks`
22. `namesort_bams`
23. `Genrich_peaks`
24. `plotFingerprint`
25. `plotFingerprint_allelic`
26. `MACS2_peak_qc`
27. `CSAW`
28. `calc_matrix_log2r_CSAW`
29. `plot_heatmap_log2r_CSAW`
30. `calc_matrix_cov_CSAW`
31. `plot_heatmap_cov_CSAW`
32. `CSAW_report`
33. `get_nearest_transcript`
34. `get_nearest_gene`
35. `split_sampleSheet`
36. `filter_gtf`
37. `gtf_to_files`
38. `annotation_bed2fasta`
39. `all`
