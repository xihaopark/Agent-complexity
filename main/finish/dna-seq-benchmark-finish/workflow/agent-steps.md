# dna-seq-benchmark-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__dna-seq-benchmark`
- Source snakefile: `../workflow_candidates/snakemake-workflows__dna-seq-benchmark/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `eval`
2. `norm_vcf`
3. `index_vcf`
4. `index_bcf`
5. `sort_vcf`
6. `get_reads`
7. `get_archive`
8. `get_truth`
9. `rename_truth_contigs`
10. `merge_truthsets`
11. `normalize_truth`
12. `get_confidence_bed`
13. `get_liftover_track`
14. `get_target_bed`
15. `postprocess_target_bed`
16. `get_reference`
17. `get_liftover_chain`
18. `samtools_faidx`
19. `bwa_index`
20. `bwa_mem`
21. `mark_duplicates`
22. `samtools_index`
23. `mosdepth`
24. `stratify_regions`
25. `get_reference_dict`
26. `merge_callsets`
27. `liftover_callset`
28. `rename_contigs`
29. `add_format_field`
30. `remove_non_pass`
31. `intersect_calls_with_target_regions`
32. `restrict_to_reference_contigs`
33. `normalize_calls`
34. `stratify_truth`
35. `stratify_results`
36. `index_stratified_truth`
37. `stat_truth`
38. `generate_sdf`
39. `benchmark_variants_germline`
40. `benchmark_variants_somatic`
41. `extract_fp_fn`
42. `extract_fp_fn_tp`
43. `reformat_fp_fn_tp_tables`
44. `calc_precision_recall`
45. `collect_stratifications`
46. `collect_precision_recall`
47. `report_precision_recall`
48. `collect_fp_fn`
49. `collect_stratifications_fp_fn`
50. `collect_fp_fn_benchmark`
51. `filter_shared_fn`
52. `filter_unique`
53. `write_shared_fn_vcf`
54. `write_unique_fn_vcf`
55. `write_unique_fp_vcf`
56. `report_fp_fn`
57. `report_fp_fn_callset`
58. `get_downsampled_vep_cache`
59. `get_vep_cache`
60. `get_vep_plugins`
61. `download_revel`
62. `process_revel_scores`
63. `tabix_revel_scores`
64. `annotate_shared_fn`
65. `annotate_unique_fp_fn`
66. `vembrane_table_shared_fn`
67. `vembrane_table_unique_fp_fn`
68. `all`
