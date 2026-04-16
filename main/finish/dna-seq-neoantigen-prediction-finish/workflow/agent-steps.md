# dna-seq-neoantigen-prediction-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__dna-seq-neoantigen-prediction`
- Source snakefile: `../workflow_candidates/snakemake-workflows__dna-seq-neoantigen-prediction/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `bcf_index`
2. `bam_index`
3. `tabix_known_variants`
4. `gzip_fastq`
5. `tsv_to_excel`
6. `get_sra`
7. `cutadapt_pipe`
8. `cutadapt_pe`
9. `cutadapt_se`
10. `merge_fastqs`
11. `get_genome`
12. `get_cdna`
13. `kallisto_index`
14. `get_annotation`
15. `STAR_index`
16. `split_annotation`
17. `genome_faidx`
18. `genome_dict`
19. `get_callregions`
20. `get_known_variants`
21. `remove_iupac_codes`
22. `bwa_index`
23. `download_HLALA_graph`
24. `index_HLALA`
25. `get_vep_cache`
26. `get_vep_plugins`
27. `make_sampleheader`
28. `map_reads`
29. `mark_duplicates`
30. `recalibrate_base_qualities`
31. `apply_bqsr`
32. `strelka_somatic`
33. `strelka_germline`
34. `vcf_to_bcf`
35. `concat_somatic`
36. `get_tumor_from_somatic`
37. `reheader_germline`
38. `concat_variants`
39. `preprocess_variants`
40. `norm_vcf`
41. `freebayes`
42. `scatter_candidates`
43. `render_scenario`
44. `varlociraptor_preprocess`
45. `varlociraptor_call`
46. `sort_calls`
47. `bcftools_concat`
48. `annotate_variants`
49. `annotate_strelka_variants`
50. `filter_by_annotation`
51. `filter_odds`
52. `gather_calls`
53. `control_fdr`
54. `merge_calls`
55. `change_samplenames`
56. `reheader_varlociraptor`
57. `microphaser_somatic`
58. `microphaser_germline`
59. `concat_proteome`
60. `build_germline_proteome`
61. `microphaser_filter`
62. `concat_tsvs`
63. `HLA_LA`
64. `parse_HLA_LA`
65. `razers3`
66. `bam2fq`
67. `OptiType`
68. `parse_Optitype`
69. `netMHCpan`
70. `netMHCIIpan`
71. `parse_mhc_out`
72. `mhc_csv_table`
73. `add_RNA_info`
74. `kallisto_quant`
75. `STAR_align`
76. `arriba`
77. `estimate_tmb`
78. `vg2svg`
79. `all`
