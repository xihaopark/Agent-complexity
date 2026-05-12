# Evaluation V2 · batch `sweep_v3_pipeline_20260416T194356Z`

evaluator_version: `v2` · ts: `2026-04-16T20:26:57Z` · n_tasks: 32 · rtol=0.001 atol=1e-05

**Mean overall score:** 0.763

**Verdict counts (V2):** pass=17, partial_pass=5, partial_fail=6, fail=4, error=0

**Verdict counts (legacy V1):** pass=15, partial=13, fail=4

| task | verdict | verdict (V1) | overall | process_mean | files_mean | n_expected | strategies |
|------|---------|--------------|---------|--------------|------------|------------|------------|
| `akinyi_deseq2` | **pass** | pass | 1.000 | 1.00 | 1.000 | 2 | byte_identical |
| `star_deseq2_init` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `star_deseq2_contrast` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `methylkit_load` | **fail** | fail | 0.150 | 0.50 | 0.000 | 1 | missing |
| `methylkit_unite` | **fail** | fail | 0.075 | 0.25 | 0.000 | 1 | missing |
| `methylkit_to_tibble` | **fail** | fail | 0.225 | 0.75 | 0.000 | 1 | missing |
| `longseq_deseq2_init` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `longseq_deseq2_contrast` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `snakepipes_merge_fc` | **partial_fail** | partial | 0.475 | 1.00 | 0.250 | 1 | process_credit |
| `snakepipes_merge_ct` | **partial_fail** | partial | 0.475 | 1.00 | 0.250 | 1 | process_credit |
| `riya_limma` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `chipseq_plot_macs_qc` | **partial_fail** | partial | 0.475 | 1.00 | 0.250 | 1 | process_credit |
| `chipseq_plot_homer_annot` | **partial_fail** | partial | 0.475 | 1.00 | 0.250 | 1 | process_credit |
| `snakepipes_scrna_merge_coutt` | **partial_pass** | partial | 0.734 | 1.00 | 0.620 | 2 | process_credit,tabular_tolerance |
| `snakepipes_scrna_qc` | **pass** | pass | 1.000 | 1.00 | 1.000 | 2 | byte_identical |
| `spilterlize_filter_features` | **partial_pass** | partial | 0.900 | 1.00 | 0.857 | 1 | tabular_tolerance |
| `spilterlize_norm_voom` | **partial_pass** | partial | 0.900 | 1.00 | 0.857 | 1 | tabular_tolerance |
| `spilterlize_limma_rbe` | **pass** | partial | 0.993 | 1.00 | 0.990 | 1 | tabular_tolerance |
| `spilterlize_norm_edger` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `dea_limma` | **partial_pass** | partial | 0.734 | 1.00 | 0.620 | 2 | process_credit,tabular_tolerance |
| `msisensor_merge` | **pass** | partial | 0.993 | 1.00 | 0.990 | 1 | tabular_tolerance |
| `methylkit_filt_norm` | **fail** | fail | 0.225 | 0.75 | 0.000 | 1 | missing |
| `methylkit2tibble_split` | **partial_pass** | partial | 0.650 | 1.00 | 0.500 | 1 | tabular_tolerance |
| `methylkit_remove_snvs` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `phantompeak_correlation` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | normalized_text_equal |
| `nearest_gene` | **partial_fail** | partial | 0.475 | 1.00 | 0.250 | 1 | process_credit |
| `chipseq_plot_frip_score` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `chipseq_plot_peaks_count_macs2` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | normalized_table_equal |
| `chipseq_plot_annotatepeaks_summary_homer` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `epibtn_rpkm` | **partial_fail** | partial | 0.475 | 1.00 | 0.250 | 1 | process_credit |
| `snakepipes_scrna_report` | **pass** | pass | 1.000 | 1.00 | 1.000 | 1 | byte_identical |
| `clean_histoneHMM` | **pass** | pass | 1.000 | 1.00 | 1.000 | 2 | byte_identical |

## Per-file detail

### `akinyi_deseq2`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `deseq2_up.txt` | byte_identical | 1.000 | True | 2481 | 2481 |
| `deseq2_down.txt` | byte_identical | 1.000 | True | 1524 | 1524 |

### `star_deseq2_init`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `normalized_counts.tsv` | byte_identical | 1.000 | True | 58217 | 58217 |

### `star_deseq2_contrast`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `contrast_results.tsv` | byte_identical | 1.000 | True | 53764 | 53764 |

### `methylkit_load`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `mk_raw.rds` | missing | 0.000 | False | None | 3529 |

### `methylkit_unite`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `unite_stats.tsv` | missing | 0.000 | False | None | 83 |

### `methylkit_to_tibble`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `mean_mcpg.tsv` | missing | 0.000 | False | None | 406 |

### `longseq_deseq2_init`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `normalized_counts.tsv` | byte_identical | 1.000 | True | 56240 | 56240 |

### `longseq_deseq2_contrast`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `contrast_results.tsv` | byte_identical | 1.000 | True | 50518 | 50518 |

### `snakepipes_merge_fc`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `merged_counts.tsv` | process_credit | 0.250 | False | 13052 | 11553 |

### `snakepipes_merge_ct`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `merged_tpm.tsv` | process_credit | 0.250 | False | 14268 | 13171 |

### `riya_limma`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `deg_results.csv` | byte_identical | 1.000 | True | 27697 | 27697 |

### `chipseq_plot_macs_qc`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `macs_qc_summary.tsv` | process_credit | 0.250 | False | 2033 | 824 |

### `chipseq_plot_homer_annot`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `homer_annot_summary.tsv` | process_credit | 0.250 | False | 139 | 143 |

### `snakepipes_scrna_merge_coutt`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `merged_coutt.tsv` | tabular_tolerance | 0.990 | False | 9042 | 9234 |
| `merged_coutt.cell_names.tsv` | process_credit | 0.250 | False | 781 | 868 |

### `snakepipes_scrna_qc`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `scqc.libstats_reads.tsv` | byte_identical | 1.000 | True | 144 | 144 |
| `scqc.libstats_pct.tsv` | byte_identical | 1.000 | True | 128 | 128 |

### `spilterlize_filter_features`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `filtered_counts.csv` | tabular_tolerance | 0.857 | False | 11932 | 14840 |

### `spilterlize_norm_voom`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `normalized_counts.csv` | tabular_tolerance | 0.857 | False | 31507 | 33715 |

### `spilterlize_limma_rbe`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `integrated_data.csv` | tabular_tolerance | 0.990 | False | 21188 | 21188 |

### `spilterlize_norm_edger`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `all/normTMM.csv` | byte_identical | 1.000 | True | 33698 | 33698 |

### `dea_limma`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `dea_results.csv` | process_credit | 0.250 | False | 48523 | 56606 |
| `model_matrix.csv` | tabular_tolerance | 0.990 | False | 107 | 107 |

### `msisensor_merge`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `merged_msi.tsv` | tabular_tolerance | 0.990 | False | 103 | 103 |

### `methylkit_filt_norm`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `filt_norm_stats.tsv` | missing | 0.000 | False | None | 211 |

### `methylkit2tibble_split`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `mean_mcpg_split.tsv` | tabular_tolerance | 0.500 | False | 225 | 345 |

### `methylkit_remove_snvs`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `snv_stats.tsv` | byte_identical | 1.000 | True | 45 | 45 |

### `phantompeak_correlation`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `crosscorr.csv` | normalized_text_equal | 1.000 | False | 295 | 296 |

### `nearest_gene`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `annotated.bed` | process_credit | 0.250 | False | 4814 | 5118 |

### `chipseq_plot_frip_score`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `frip_scores.tsv` | byte_identical | 1.000 | True | 120 | 120 |

### `chipseq_plot_peaks_count_macs2`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `peaks_count.tsv` | normalized_table_equal | 1.000 | False | 117 | 105 |

### `chipseq_plot_annotatepeaks_summary_homer`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `homer_long.tsv` | byte_identical | 1.000 | True | 330 | 330 |

### `epibtn_rpkm`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `results/RNA/DEG/genes_rpkm__runX__mockref.txt` | process_credit | 0.250 | False | 16 | 11131 |

### `snakepipes_scrna_report`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `scrna_report.tsv` | byte_identical | 1.000 | True | 299 | 299 |

### `clean_histoneHMM`

| file | strategy | score | bytes_eq | size_a | size_r |
|------|----------|-------|----------|--------|--------|
| `sampleA_avgp0.5.bed` | byte_identical | 1.000 | True | 1120 | 1120 |
| `sampleB_avgp0.5.bed` | byte_identical | 1.000 | True | 1020 | 1020 |
