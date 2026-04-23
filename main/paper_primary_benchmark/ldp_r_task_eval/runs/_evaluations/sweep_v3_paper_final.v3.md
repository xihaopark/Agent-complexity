# Evaluation V3 · batch `sweep_v3_paper_final`

evaluator_version: `v3` · ts: `2026-04-17T01:16:22Z` · n_tasks: 32 · rtol=0.001 atol=1e-05

**Mean overall score:** 0.784

**Verdict counts (V2):** pass=21, partial_pass=1, partial_fail=6, fail=4, error=0

**Failure-mode distribution (V3):** mixed=1, ok=21, row_drift=3, rscript_crashed=4, schema_drift=3

**Confidence distribution (V3):** high=20, medium=3, low=9

| task | verdict | overall | failure_mode | confidence | insight |
|------|---------|---------|--------------|------------|---------|
| `akinyi_deseq2` | pass | 1.000 | **ok** | high | `deseq2_up.txt`: byte-identical ; `deseq2_down.txt`: byte-identical |
| `star_deseq2_init` | pass | 1.000 | **ok** | high | `normalized_counts.tsv`: byte-identical |
| `star_deseq2_contrast` | pass | 1.000 | **ok** | high | `contrast_results.tsv`: byte-identical |
| `methylkit_load` | fail | 0.075 | **rscript_crashed** | low | `mk_raw.rds`: file missing |
| `methylkit_unite` | fail | 0.075 | **rscript_crashed** | low | `unite_stats.tsv`: file missing |
| `methylkit_to_tibble` | fail | 0.225 | **rscript_crashed** | low | `mean_mcpg.tsv`: file missing |
| `longseq_deseq2_init` | pass | 1.000 | **ok** | high | `normalized_counts.tsv`: byte-identical |
| `longseq_deseq2_contrast` | pass | 1.000 | **ok** | high | `contrast_results.tsv`: byte-identical |
| `snakepipes_merge_fc` | partial_fail | 0.475 | **schema_drift** | low | `merged_counts.tsv`: column count 6 vs ref 5 (shared 5) |
| `snakepipes_merge_ct` | partial_fail | 0.475 | **schema_drift** | low | `merged_tpm.tsv`: column count 6 vs ref 5 (shared 5) |
| `riya_limma` | pass | 0.993 | **ok** | high | `deg_results.csv`: ≥95% cells equal under tolerance (float drift; score 0.99) |
| `chipseq_plot_macs_qc` | pass | 0.993 | **ok** | high | `macs_qc_summary.tsv`: ≥95% cells equal under tolerance (float drift; score 0.99) |
| `chipseq_plot_homer_annot` | partial_fail | 0.475 | **schema_drift** | low | `homer_annot_summary.tsv`: column count 4 vs ref 9 (shared 4) |
| `snakepipes_scrna_merge_coutt` | partial_pass | 0.734 | **row_drift** | high | `merged_coutt.tsv`: ≥95% cells equal under tolerance (float drift; score 0.99) ; `merged_coutt.cell_names.tsv`: schema-aligned, cells 20%, rows 0% (score 0.25) |
| `snakepipes_scrna_qc` | pass | 1.000 | **ok** | high | `scqc.libstats_reads.tsv`: byte-identical ; `scqc.libstats_pct.tsv`: byte-identical |
| `spilterlize_filter_features` | pass | 1.000 | **ok** | high | `filtered_counts.csv`: byte-identical |
| `spilterlize_norm_voom` | pass | 1.000 | **ok** | high | `normalized_counts.csv`: byte-identical |
| `spilterlize_limma_rbe` | pass | 1.000 | **ok** | high | `integrated_data.csv`: byte-identical |
| `spilterlize_norm_edger` | pass | 1.000 | **ok** | high | `all/normTMM.csv`: byte-identical |
| `dea_limma` | partial_fail | 0.562 | **mixed** | medium | `dea_results.csv`: column count 8 vs ref 9 (shared 8) ; `model_matrix.csv`: schema-aligned, cells 50%, rows 0% (score 0.50) |
| `msisensor_merge` | pass | 0.993 | **ok** | high | `merged_msi.tsv`: ≥95% cells equal under tolerance (float drift; score 0.99) |
| `methylkit_filt_norm` | pass | 0.993 | **ok** | high | `filt_norm_stats.tsv`: ≥95% cells equal under tolerance (float drift; score 0.99) |
| `methylkit2tibble_split` | fail | 0.075 | **rscript_crashed** | low | `mean_mcpg_split.tsv`: file missing |
| `methylkit_remove_snvs` | pass | 1.000 | **ok** | medium | `snv_stats.tsv`: tolerant equal (normalized_table_equal) |
| `phantompeak_correlation` | pass | 0.993 | **ok** | high | `crosscorr.csv`: ≥95% cells equal under tolerance (float drift; score 0.99) |
| `nearest_gene` | partial_fail | 0.475 | **row_drift** | low | `annotated.bed`: file present 4903B vs ref 5118B, unparseable by V2 ladder (process credit 0.25) |
| `chipseq_plot_frip_score` | pass | 0.993 | **ok** | high | `frip_scores.tsv`: ≥95% cells equal under tolerance (float drift; score 0.99) |
| `chipseq_plot_peaks_count_macs2` | pass | 1.000 | **ok** | medium | `peaks_count.tsv`: tolerant equal (normalized_table_equal) |
| `chipseq_plot_annotatepeaks_summary_homer` | pass | 1.000 | **ok** | high | `homer_long.tsv`: byte-identical |
| `epibtn_rpkm` | partial_fail | 0.475 | **row_drift** | low | `results/RNA/DEG/genes_rpkm__runX__mockref.txt`: row count 1 vs ref 360 (359 diff), cells≈0.00 |
| `snakepipes_scrna_report` | pass | 1.000 | **ok** | high | `scrna_report.tsv`: byte-identical |
| `clean_histoneHMM` | pass | 1.000 | **ok** | high | `sampleA_avgp0.5.bed`: byte-identical ; `sampleB_avgp0.5.bed`: byte-identical |

## Why (actionable fix per task)

### `akinyi_deseq2` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `deseq2_up.txt` [ok]: byte-identical
- `deseq2_down.txt` [ok]: byte-identical

### `star_deseq2_init` — ok (high)

- fix: no action needed
- skill tokens matched: 3/3 (DESeq, DESeq2, DESeqDataSetFromMatrix)
- `normalized_counts.tsv` [ok]: byte-identical

### `star_deseq2_contrast` — ok (high)

- fix: no action needed
- skill tokens matched: 2/3 (DESeq, DESeq2)
- `contrast_results.tsv` [ok]: byte-identical

### `methylkit_load` — rscript_crashed (low)

- fix: R error: Error in if (is.na(treatment)) stop("Treatment vector is missing.") :
- skill tokens matched: 0/0
- `mk_raw.rds` [output_missing]: file missing
- last R error: `Error in if (is.na(treatment)) stop("Treatment vector is missing.") :`

### `methylkit_unite` — rscript_crashed (low)

- fix: R error: Error in if (is.na(treatment)) stop("Treatment vector is missing.") :
- skill tokens matched: 0/0
- `unite_stats.tsv` [output_missing]: file missing
- last R error: `Error in if (is.na(treatment)) stop("Treatment vector is missing.") :`

### `methylkit_to_tibble` — rscript_crashed (low)

- fix: R error: Error in `group_by()`:
- skill tokens matched: 0/0
- `mean_mcpg.tsv` [output_missing]: file missing
- last R error: `Error in `group_by()`:`

### `longseq_deseq2_init` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `normalized_counts.tsv` [ok]: byte-identical

### `longseq_deseq2_contrast` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `contrast_results.tsv` [ok]: byte-identical
- last R error: `Error in lfcShrink(dds, coef = "condition_ko_vs_wt", type = "ashr", res = res) :`

### `snakepipes_merge_fc` — schema_drift (low)

- fix: produced 6 cols vs reference 5 (shared 5) on `merged_counts.tsv`
- skill tokens matched: 0/0
- `merged_counts.tsv` [schema_drift]: column count 6 vs ref 5 (shared 5)

### `snakepipes_merge_ct` — schema_drift (low)

- fix: produced 6 cols vs reference 5 (shared 5) on `merged_tpm.tsv`
- skill tokens matched: 0/0
- `merged_tpm.tsv` [schema_drift]: column count 6 vs ref 5 (shared 5)

### `riya_limma` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `deg_results.csv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)

### `chipseq_plot_macs_qc` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `macs_qc_summary.tsv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)

### `chipseq_plot_homer_annot` — schema_drift (low)

- fix: produced 4 cols vs reference 9 (shared 4) on `homer_annot_summary.tsv`
- skill tokens matched: 0/0
- `homer_annot_summary.tsv` [schema_drift]: column count 4 vs ref 9 (shared 4)

### `snakepipes_scrna_merge_coutt` — row_drift (high)

- fix: cells matched 3000/3000 (100%) on `merged_coutt.tsv`
- skill tokens matched: 0/0
- `merged_coutt.tsv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)
- `merged_coutt.cell_names.tsv` [row_drift]: schema-aligned, cells 20%, rows 0% (score 0.25)

### `snakepipes_scrna_qc` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `scqc.libstats_reads.tsv` [ok]: byte-identical
- `scqc.libstats_pct.tsv` [ok]: byte-identical

### `spilterlize_filter_features` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `filtered_counts.csv` [ok]: byte-identical

### `spilterlize_norm_voom` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `normalized_counts.csv` [ok]: byte-identical

### `spilterlize_limma_rbe` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `integrated_data.csv` [ok]: byte-identical

### `spilterlize_norm_edger` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `all/normTMM.csv` [ok]: byte-identical
- last R error: `Error in fwrite(as.data.frame(log_cpm), file = "output/all/normTMM.csv",  :`

### `dea_limma` — mixed (medium)

- fix: multiple failure modes across expected files — see per-file diff
- skill tokens matched: 4/4 (eBayes, lmFit, model.matrix, topTable)
- `dea_results.csv` [schema_drift]: column count 8 vs ref 9 (shared 8)
- `model_matrix.csv` [row_drift]: schema-aligned, cells 50%, rows 0% (score 0.50)

### `msisensor_merge` — ok (high)

- fix: no action needed
- skill tokens matched: 0/2
- `merged_msi.tsv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)

### `methylkit_filt_norm` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `filt_norm_stats.tsv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)
- last R error: `Error in FUN(X[[i]], ...) :`

### `methylkit2tibble_split` — rscript_crashed (low)

- fix: R error: Error:
- skill tokens matched: 0/0
- `mean_mcpg_split.tsv` [output_missing]: file missing
- last R error: `Error:`

### `methylkit_remove_snvs` — ok (medium)

- fix: no action needed
- skill tokens matched: 0/0
- `snv_stats.tsv` [ok]: tolerant equal (normalized_table_equal)

### `phantompeak_correlation` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `crosscorr.csv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)

### `nearest_gene` — row_drift (low)

- fix: content drift across rows
- skill tokens matched: 0/0
- `annotated.bed` [row_drift]: file present 4903B vs ref 5118B, unparseable by V2 ladder (process credit 0.25)

### `chipseq_plot_frip_score` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `frip_scores.tsv` [ok]: ≥95% cells equal under tolerance (float drift; score 0.99)

### `chipseq_plot_peaks_count_macs2` — ok (medium)

- fix: no action needed
- skill tokens matched: 0/0
- `peaks_count.tsv` [ok]: tolerant equal (normalized_table_equal)

### `chipseq_plot_annotatepeaks_summary_homer` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `homer_long.tsv` [ok]: byte-identical

### `epibtn_rpkm` — row_drift (low)

- fix: cells matched 0/3 (0%) on `results/RNA/DEG/genes_rpkm__runX__mockref.txt`
- skill tokens matched: 0/0
- `results/RNA/DEG/genes_rpkm__runX__mockref.txt` [row_drift]: row count 1 vs ref 360 (359 diff), cells≈0.00
- last R error: `Error in `select()`:`

### `snakepipes_scrna_report` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `scrna_report.tsv` [ok]: byte-identical

### `clean_histoneHMM` — ok (high)

- fix: no action needed
- skill tokens matched: 0/0
- `sampleA_avgp0.5.bed` [ok]: byte-identical
- `sampleB_avgp0.5.bed` [ok]: byte-identical
