# Evaluation V3 · batch `sweep_v3_pipeline_20260416T194356Z`

evaluator_version: `v3` · ts: `2026-04-17T01:25:50Z` · n_tasks: 32 · rtol=0.001 atol=1e-05

**Mean overall score:** 0.818

**Verdict counts (V2):** pass=17, partial_pass=9, partial_fail=2, fail=4, error=0

**Failure-mode distribution (V3):** infinite_debug_loop=1, ok=17, row_drift=5, rscript_crashed=4, schema_drift=5

**Confidence distribution (V3):** high=17, medium=9, low=6

| task | verdict | overall | failure_mode | confidence | insight |
|------|---------|---------|--------------|------------|---------|
| `akinyi_deseq2` | pass | 1.000 | **ok** | high | `deseq2_up.txt`: byte-identical ; `deseq2_down.txt`: byte-identical |
| `star_deseq2_init` | pass | 1.000 | **ok** | high | `normalized_counts.tsv`: byte-identical |
| `star_deseq2_contrast` | pass | 1.000 | **ok** | high | `contrast_results.tsv`: byte-identical |
| `methylkit_load` | fail | 0.150 | **rscript_crashed** | low | `mk_raw.rds`: file missing |
| `methylkit_unite` | fail | 0.075 | **rscript_crashed** | low | `unite_stats.tsv`: file missing |
| `methylkit_to_tibble` | fail | 0.225 | **rscript_crashed** | low | `mean_mcpg.tsv`: file missing |
| `longseq_deseq2_init` | pass | 1.000 | **ok** | high | `normalized_counts.tsv`: byte-identical |
| `longseq_deseq2_contrast` | pass | 1.000 | **ok** | high | `contrast_results.tsv`: byte-identical |
| `snakepipes_merge_fc` | partial_pass | 0.831 | **schema_drift** | medium | `merged_counts.tsv`: column count 6 vs ref 5 (shared 5) |
| `snakepipes_merge_ct` | partial_pass | 0.832 | **schema_drift** | medium | `merged_tpm.tsv`: column count 6 vs ref 5 (shared 5) |
| `riya_limma` | pass | 1.000 | **ok** | high | `deg_results.csv`: byte-identical |
| `chipseq_plot_macs_qc` | partial_fail | 0.598 | **schema_drift** | low | `macs_qc_summary.tsv`: column count 3 vs ref 9 (shared 2) |
| `chipseq_plot_homer_annot` | partial_pass | 0.746 | **schema_drift** | medium | `homer_annot_summary.tsv`: column count 4 vs ref 9 (shared 4) |
| `snakepipes_scrna_merge_coutt` | partial_pass | 0.734 | **row_drift** | high | `merged_coutt.tsv`: ≥95% cells equal under tolerance (float drift; score 0.99) ; `merged_coutt.cell_names.tsv`: schema-aligned, cells 20%, rows 0% (score 0.25) |
| `snakepipes_scrna_qc` | pass | 1.000 | **ok** | high | `scqc.libstats_reads.tsv`: byte-identical ; `scqc.libstats_pct.tsv`: byte-identical |
| `spilterlize_filter_features` | partial_pass | 0.900 | **row_drift** | medium | `filtered_counts.csv`: schema-aligned, cells 86%, rows 0% (score 0.86) |
| `spilterlize_norm_voom` | partial_pass | 0.900 | **row_drift** | medium | `normalized_counts.csv`: schema-aligned, cells 86%, rows 0% (score 0.86) |
| `spilterlize_limma_rbe` | pass | 0.993 | **ok** | high | `integrated_data.csv`: ≥95% cells equal under tolerance (float drift; score 0.99) |
| `spilterlize_norm_edger` | pass | 1.000 | **ok** | high | `all/normTMM.csv`: byte-identical |
| `dea_limma` | partial_pass | 0.854 | **schema_drift** | high | `dea_results.csv`: column count 8 vs ref 9 (shared 8) ; `model_matrix.csv`: ≥95% cells equal under tolerance (float drift; score 0.99) |
| `msisensor_merge` | pass | 0.993 | **ok** | high | `merged_msi.tsv`: ≥95% cells equal under tolerance (float drift; score 0.99) |
| `methylkit_filt_norm` | fail | 0.225 | **rscript_crashed** | low | `filt_norm_stats.tsv`: file missing |
| `methylkit2tibble_split` | partial_pass | 0.746 | **infinite_debug_loop** | medium | `mean_mcpg_split.tsv`: row count 6 vs ref 12 (6 diff), cells≈0.75 |
| `methylkit_remove_snvs` | pass | 1.000 | **ok** | high | `snv_stats.tsv`: byte-identical |
| `phantompeak_correlation` | pass | 1.000 | **ok** | medium | `crosscorr.csv`: tolerant equal (normalized_text_equal) |
| `nearest_gene` | partial_pass | 0.889 | **row_drift** | medium | `annotated.bed`: schema-aligned, cells 84%, rows 0% (score 0.84) |
| `chipseq_plot_frip_score` | pass | 1.000 | **ok** | high | `frip_scores.tsv`: byte-identical |
| `chipseq_plot_peaks_count_macs2` | pass | 1.000 | **ok** | medium | `peaks_count.tsv`: tolerant equal (normalized_table_equal) |
| `chipseq_plot_annotatepeaks_summary_homer` | pass | 1.000 | **ok** | high | `homer_long.tsv`: byte-identical |
| `epibtn_rpkm` | partial_fail | 0.475 | **row_drift** | low | `results/RNA/DEG/genes_rpkm__runX__mockref.txt`: row count 1 vs ref 360 (359 diff), cells≈0.00 |
| `snakepipes_scrna_report` | pass | 1.000 | **ok** | high | `scrna_report.tsv`: byte-identical |
| `clean_histoneHMM` | pass | 1.000 | **ok** | high | `sampleA_avgp0.5.bed`: byte-identical ; `sampleB_avgp0.5.bed`: byte-identical |

## Why (actionable fix per task)

### `akinyi_deseq2` — ok (high)

- fix: no action needed
- skill tokens matched: 13/22 (DESeq, DESeq2, DESeqDataSetFromMatrix, as.data.frame, as.factor, as.matrix...)
- `deseq2_up.txt` [ok]: byte-identical
- `deseq2_down.txt` [ok]: byte-identical

### `star_deseq2_init` — ok (high)

- fix: no action needed
- skill tokens matched: 8/34 (DESeq, DESeqDataSetFromMatrix, condition, data.frame, rownames, samples.tsv...)
- `normalized_counts.tsv` [ok]: byte-identical

### `star_deseq2_contrast` — ok (high)

- fix: no action needed
- skill tokens matched: 6/34 (DESeq, condition, data.frame, lfcShrink, readRDS, rownames)
- `contrast_results.tsv` [ok]: byte-identical

### `methylkit_load` — rscript_crashed (low)

- fix: R error: Error in if (is.na(treatment)) stop("Treatment vector is missing.") :
- skill tokens matched: 2/38 (METHYLKIT, methylKit)
- `mk_raw.rds` [output_missing]: file missing
- last R error: `Error in if (is.na(treatment)) stop("Treatment vector is missing.") :`

### `methylkit_unite` — rscript_crashed (low)

- fix: R error: Error in if (is.na(treatment)) stop("Treatment vector is missing.") :
- skill tokens matched: 2/38 (METHYLKIT, methylKit)
- `unite_stats.tsv` [output_missing]: file missing
- last R error: `Error in if (is.na(treatment)) stop("Treatment vector is missing.") :`

### `methylkit_to_tibble` — rscript_crashed (low)

- fix: R error: Error in `mutate()`:
- skill tokens matched: 3/38 (METHYLKIT, as_tibble, methylKit)
- `mean_mcpg.tsv` [output_missing]: file missing
- last R error: `Error in `mutate()`:`

### `longseq_deseq2_init` — ok (high)

- fix: no action needed
- skill tokens matched: 5/42 (DESeq, DESeqDataSetFromMatrix, data.frame, rownames, saveRDS)
- `normalized_counts.tsv` [ok]: byte-identical

### `longseq_deseq2_contrast` — ok (high)

- fix: no action needed
- skill tokens matched: 5/42 (DESeq, data.frame, lfcShrink, readRDS, rownames)
- `contrast_results.tsv` [ok]: byte-identical

### `snakepipes_merge_fc` — schema_drift (medium)

- fix: produced 6 cols vs reference 5 (shared 5) on `merged_counts.tsv`
- skill tokens matched: 0/18
- `merged_counts.tsv` [schema_drift]: column count 6 vs ref 5 (shared 5)

### `snakepipes_merge_ct` — schema_drift (medium)

- fix: produced 6 cols vs reference 5 (shared 5) on `merged_tpm.tsv`
- skill tokens matched: 0/18
- `merged_tpm.tsv` [schema_drift]: column count 6 vs ref 5 (shared 5)
- last R error: `Error in write.table(merged_tpm, file = "output/merged_tpm.tsv", sep = "\t",  :`

### `riya_limma` — ok (high)

- fix: no action needed
- skill tokens matched: 8/31 (colnames, contrasts.fit, eBayes, lmFit, makeContrasts, model.matrix...)
- `deg_results.csv` [ok]: byte-identical

### `chipseq_plot_macs_qc` — schema_drift (low)

- fix: produced 3 cols vs reference 9 (shared 2) on `macs_qc_summary.tsv`
- skill tokens matched: 1/35 (read.delim)
- `macs_qc_summary.tsv` [schema_drift]: column count 3 vs ref 9 (shared 2)
- last R error: `Error in pivot_longer(., cols = everything(), names_to = "measure", values_to = "value") :`

### `chipseq_plot_homer_annot` — schema_drift (medium)

- fix: produced 4 cols vs reference 9 (shared 4) on `homer_annot_summary.tsv`
- skill tokens matched: 1/35 (read.delim)
- `homer_annot_summary.tsv` [schema_drift]: column count 4 vs ref 9 (shared 4)
- last R error: `Error in reduce(list(a_features, b_features, c_features), full_join, by = "Feature") :`

### `snakepipes_scrna_merge_coutt` — row_drift (high)

- fix: cells matched 3000/3000 (100%) on `merged_coutt.tsv`
- skill tokens matched: 0/18
- `merged_coutt.tsv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)
- `merged_coutt.cell_names.tsv` [row_drift]: schema-aligned, cells 20%, rows 0% (score 0.25)

### `snakepipes_scrna_qc` — ok (high)

- fix: no action needed
- skill tokens matched: 0/18
- `scqc.libstats_reads.tsv` [ok]: byte-identical
- `scqc.libstats_pct.tsv` [ok]: byte-identical

### `spilterlize_filter_features` — row_drift (medium)

- fix: cells matched 2400/2800 (86%) on `filtered_counts.csv`
- skill tokens matched: 3/27 (annotation, filterByExpr, row.names)
- `filtered_counts.csv` [row_drift]: schema-aligned, cells 86%, rows 0% (score 0.86)
- last R error: `Error in fread("input/counts.csv", header = TRUE, row.names = 1) :`

### `spilterlize_norm_voom` — row_drift (medium)

- fix: cells matched 1800/2100 (86%) on `normalized_counts.csv`
- skill tokens matched: 3/27 (CalcNormFactors, data.frame, row.names)
- `normalized_counts.csv` [row_drift]: schema-aligned, cells 86%, rows 0% (score 0.86)
- last R error: `Error in fread("input/filtered_counts.csv", header = TRUE, row.names = 1) :`

### `spilterlize_limma_rbe` — ok (high)

- fix: no action needed
- skill tokens matched: 3/27 (annotation, removeBatchEffect, row.names)
- `integrated_data.csv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)
- last R error: `Error in fread("input/normalized.csv", header = TRUE, row.names = 1) :`

### `spilterlize_norm_edger` — ok (high)

- fix: no action needed
- skill tokens matched: 3/27 (CalcNormFactors, data.frame, row.names)
- `all/normTMM.csv` [ok]: byte-identical
- last R error: `Error in fwrite(as.data.frame(log_cpm), "output/all/normTMM.csv", row.names = TRUE) :`

### `dea_limma` — schema_drift (high)

- fix: produced 8 cols vs reference 9 (shared 8) on `dea_results.csv`
- skill tokens matched: 11/28 (DGEList, calcNormFactors, data.frame, eBayes, edgeR, edgeR::calcNormFactors...)
- `dea_results.csv` [schema_drift]: column count 8 vs ref 9 (shared 8)
- `model_matrix.csv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)
- last R error: `Error in fit$coefficients[, coef] : subscript out of bounds`

### `msisensor_merge` — ok (high)

- fix: no action needed
- skill tokens matched: 3/15 (read_tsv, tidyverse, write_tsv)
- `merged_msi.tsv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)

### `methylkit_filt_norm` — rscript_crashed (low)

- fix: R error: Error: unable to find an inherited method for function ‘percMethylation’ for signature ‘methylBase.o
- skill tokens matched: 4/38 (METHYLKIT, methylKit, methylKit::percMethylation, percMethylation)
- `filt_norm_stats.tsv` [output_missing]: file missing
- last R error: `Error: unable to find an inherited method for function ‘percMethylation’ for signature ‘methylBase.obj = "methylRaw"’`

### `methylkit2tibble_split` — infinite_debug_loop (medium)

- fix: agent retried 7 times after first write; consider raising max_steps or injecting an explicit recipe
- skill tokens matched: 4/38 (METHYLKIT, as_tibble, methylKit, str_remove)
- `mean_mcpg_split.tsv` [row_drift]: row count 6 vs ref 12 (6 diff), cells≈0.75
- last R error: `Error in `pivot_wider()`:`

### `methylkit_remove_snvs` — ok (high)

- fix: no action needed
- skill tokens matched: 2/38 (METHYLKIT, methylKit)
- `snv_stats.tsv` [ok]: byte-identical
- last R error: `Error: object 'df_united' not found`

### `phantompeak_correlation` — ok (medium)

- fix: no action needed
- skill tokens matched: 2/35 (data.frame, rownames)
- `crosscorr.csv` [ok]: tolerant equal (normalized_text_equal)

### `nearest_gene` — row_drift (medium)

- fix: cells matched 740/880 (84%) on `annotated.bed`
- skill tokens matched: 0/18
- `annotated.bed` [row_drift]: schema-aligned, cells 84%, rows 0% (score 0.84)
- last R error: `Error in `left_join()`:`

### `chipseq_plot_frip_score` — ok (high)

- fix: no action needed
- skill tokens matched: 1/35 (colnames)
- `frip_scores.tsv` [ok]: byte-identical

### `chipseq_plot_peaks_count_macs2` — ok (medium)

- fix: no action needed
- skill tokens matched: 1/35 (colnames)
- `peaks_count.tsv` [ok]: tolerant equal (normalized_table_equal)

### `chipseq_plot_annotatepeaks_summary_homer` — ok (high)

- fix: no action needed
- skill tokens matched: 0/35
- `homer_long.tsv` [ok]: byte-identical

### `epibtn_rpkm` — row_drift (low)

- fix: cells matched 0/3 (0%) on `results/RNA/DEG/genes_rpkm__runX__mockref.txt`
- skill tokens matched: 1/45 (read.delim)
- `results/RNA/DEG/genes_rpkm__runX__mockref.txt` [row_drift]: row count 1 vs ref 360 (359 diff), cells≈0.00
- last R error: `Error in file(file, ifelse(append, "a", "w")) :`

### `snakepipes_scrna_report` — ok (high)

- fix: no action needed
- skill tokens matched: 0/18
- `scrna_report.tsv` [ok]: byte-identical

### `clean_histoneHMM` — ok (high)

- fix: no action needed
- skill tokens matched: 0/18
- `sampleA_avgp0.5.bed` [ok]: byte-identical
- `sampleB_avgp0.5.bed` [ok]: byte-identical
