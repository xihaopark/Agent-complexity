# single-cell-drop-seq-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__single-cell-drop-seq`
- Source snakefile: `../workflow_candidates/snakemake-workflows__single-cell-drop-seq/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `download_meta`
2. `qc`
3. `filter`
4. `map`
5. `extract`
6. `split_species`
7. `extract_species`
8. `merge`
9. `make_report`
10. `download_annotation`
11. `download_genome`
12. `rename_genome`
13. `merge_genomes`
14. `merge_annotations`
15. `curate_annotation`
16. `create_dict`
17. `reduce_gtf`
18. `create_refFlat`
19. `create_intervals`
20. `get_genomeChrBinNbits`
21. `prep_star_index`
22. `create_star_index`
23. `fastqc_barcodes`
24. `fastqc_reads`
25. `multiqc_fastqc_barcodes`
26. `multiqc_fastqc_reads`
27. `fasta_fastq_adapter`
28. `cutadapt_R1`
29. `cutadapt_R2`
30. `clean_cutadapt`
31. `repair`
32. `detect_barcodes`
33. `plot_adapter_content`
34. `multiqc_cutadapt_barcodes`
35. `multiqc_cutadapt_RNA`
36. `extend_barcode_whitelist`
37. `get_top_barcodes`
38. `get_cell_whitelist`
39. `extend_barcode_top`
40. `repair_barcodes`
41. `STAR_align`
42. `multiqc_star`
43. `pigz_unmapped`
44. `MergeBamAlignment`
45. `TagReadWithGeneExon`
46. `DetectBeadSubstitutionErrors`
47. `bead_errors_metrics`
48. `bam_hist`
49. `plot_yield`
50. `plot_knee_plot`
51. `extract_umi_expression`
52. `extract_reads_expression`
53. `SingleCellRnaSeqMetricsCollector`
54. `plot_rna_metrics`
55. `convert_long_to_mtx`
56. `compress_mtx`
57. `split_bam_species`
58. `extract_all_umi_expression`
59. `plot_barnyard`
60. `extract_umi_expression_species`
61. `extract_reads_expression_species`
62. `convert_long_to_mtx_species`
63. `compress_mtx_species`
64. `SingleCellRnaSeqMetricsCollector_species`
65. `plot_rna_metrics_species`
66. `merge_long`
67. `violine_plots`
68. `summary_stats`
69. `create_publication_text`
70. `all`
