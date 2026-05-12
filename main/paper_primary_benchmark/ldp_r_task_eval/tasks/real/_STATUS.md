# Real R-task benchmark — status report (batch B expansion)

This document summarises the expansion of the real R-centric task suite under
`ldp_r_task_eval/tasks/real/`. All task specifications and ground-truth outputs
were produced by running the original R script from the `workflow_candidates/`
source tree against deterministic synthetic inputs, via
`tools/build_real_r_tasks.py`.

## Final state

- Total ready tasks: **12** (4 pre-existing + 8 newly added in this batch)
- Every task's ground truth was produced by the actual source R script — no
  rewrites; R files are copied verbatim into `reference/script.R`.
- Registry: `ldp_r_task_eval/r_tasks/registry.real.json` (schema v3) lists all
  12 ready tasks.

## Task breakdown by family / stage / difficulty

| family    | count | tasks                                                                                         |
|-----------|------:|-----------------------------------------------------------------------------------------------|
| rna       |     4 | akinyi_deseq2, riya_limma, snakepipes_merge_fc, snakepipes_merge_ct                           |
| chipseq   |     5 | chipseq_plot_peak_intersect, chipseq_plot_macs_qc, chipseq_plot_homer_annot, epigenbutton_mapping_stats, epigenbutton_peak_stats |
| scrna     |     3 | snakepipes_scrna_merge_coutt, snakepipes_scrna_qc, smartseqtotal_violin                       |

| stage_position | count |
|----------------|------:|
| mid            |     7 |
| late           |     5 |

| difficulty | count |
|------------|------:|
| 1 (easy)   |     4 |
| 2 (medium) |     6 |
| 3 (harder) |     2 |

### Per-task classification

| task_id                         | family  | stage | diff | workflow (source)                                           | paper?       |
|---------------------------------|---------|-------|-----:|-------------------------------------------------------------|--------------|
| akinyi_deseq2                   | rna     | late  | 2    | akinyi-onyango-rna_seq_pipeline-finish                       | yes (PDF)    |
| riya_limma                      | rna     | late  | 2    | RiyaDua-cervical-cancer-snakemake-workflow                   | no           |
| snakepipes_merge_fc             | rna     | mid   | 2    | maxplanck-ie-snakepipes-finish                               | no           |
| snakepipes_merge_ct             | rna     | mid   | 2    | maxplanck-ie-snakepipes-finish                               | no           |
| chipseq_plot_peak_intersect     | chipseq | late  | 2    | snakemake-workflows-chipseq                                  | no           |
| chipseq_plot_macs_qc            | chipseq | late  | 2    | snakemake-workflows-chipseq                                  | no           |
| chipseq_plot_homer_annot        | chipseq | late  | 3    | snakemake-workflows-chipseq                                  | no           |
| snakepipes_scrna_merge_coutt    | scrna   | mid   | 2    | maxplanck-ie-snakepipes-finish                               | no           |
| snakepipes_scrna_qc             | scrna   | mid   | 3    | maxplanck-ie-snakepipes-finish                               | no           |
| epigenbutton_mapping_stats      | chipseq | mid   | 1    | joncahn-epigeneticbutton                                     | no           |
| epigenbutton_peak_stats         | chipseq | mid   | 1    | joncahn-epigeneticbutton                                     | no           |
| smartseqtotal_violin            | scrna   | late  | 1    | gersteinlab-ASTRO (SmartSeqTotal compatibility)              | no           |

## Represented workflows (6 of 30 source workflows)

1. `akinyi-onyango-rna_seq_pipeline-finish` (Akinyi-Onyango rna_seq_pipeline) — paper: *A survey of best practices for RNA-seq data analysis* (DOI 10.1186/s13059-016-0881-8, PDF downloaded). Pre-existing task.
2. `RiyaDua-cervical-cancer-snakemake-workflow` — no paper. Pre-existing task.
3. `maxplanck-ie-snakepipes-finish` (snakePipes) — no paper in map, 4 tasks covering RNA merging + scRNA merging/QC.
4. `snakemake-workflows-chipseq` — no paper in map; 3 tasks covering ChIP-seq peak visualisation & QC.
5. `joncahn-epigeneticbutton` — no paper in map; 2 tasks covering epigenetic-button summary plots.
6. `gersteinlab-ASTRO` — no paper in map; 1 task covering SmartSeq-Total benchmark violins (ASTRO compatibility tooling).

**Papers / PDFs represented:** 1 workflow carries a downloaded PDF (Akinyi rna_seq_pipeline → DOI 10.1186/s13059-016-0881-8). Boost-priority workflows with downloaded PDFs (systemPipeRdata, cellranger-multi, rna-seq-star-deseq2, read-alignment-pangenome, alevin-fry, cite-seq) all lack standalone `commandArgs`-based R scripts in their current repos (they rely on `snakemake@input/output/params` objects or pure Snakefile logic). See dropped-candidates section below.

## Methodology recap

1. Enumerated candidate R scripts via `grep -l 'commandArgs(trailingOnly'` and `grep -l 'snakemake@'` across all 30 workflows.
2. For each candidate, verified CRAN/Bioconductor dependency availability against the local R 4.5.1 install. CRAN installs performed during this batch: `optparse`, `UpSetR`, `VennDiagram`, `ggpubr` (plus already-present `gtools`, `reshape2`, `scales`, `cowplot`, `ggrepel`, etc.).
3. Classified every inspected candidate in `tools/candidate_r_scripts.csv` (path / workflow / family / stage / difficulty / has_paper / has_downloaded_pdf / libraries / deps_ok / deps_missing / feasibility_note).
4. Selected the 8 most reliable `deps_ok=true` + `commandArgs`-with-controllable-outputs candidates that also broadened family coverage.
5. For each selected script, wrote a deterministic `_gen_<id>(workdir, rng)` function that produces synthetic but realistic inputs matching the exact column schema expected by the script, plus a `_cmd_<id>(workdir, gtdir)` wrapper that writes outputs into `gtdir/reference_output/`.
6. Ran `build_real_r_tasks.py --all --force` — all 12 tasks reach `status: ready` with the reference R code executing end-to-end.
7. Updated `r_tasks/registry.real.json` (version bumped to 3).

## Dropped candidates

Most sources in `workflow_candidates/` are `snakemake@...`-driven scripts that cannot be executed standalone without a Snakemake context; a second bucket is scripts whose dependencies are too heavyweight to install in this environment. Headline rejections:

### Rejected for `snakemake@input/output/params` only
- `snakemake-workflows__chipseq`: `featurecounts_deseq2.R`, `plot_frip_score.R`, `plot_peaks_count_macs2.R`, `plot_annotatepeaks_summary_homer.R`
- `snakemake-workflows__rna-seq-star-deseq2`: `deseq2-init.R`, `deseq2.R`, `plot-pca.R`, `gene2symbol.R` (despite the workflow having a downloaded PDF)
- `snakemake-workflows__rna-seq-kallisto-sleuth`: every R script (`sleuth-*.R`, `plot-*.R`, `spia.R`, `ihw-fdr-control.R`, etc.)
- `snakemake-workflows__single-cell-rna-seq`: all 20+ scripts use `snakemake@` wildcards
- `epigen__dea_limma`: `limma.R`, `volcanos.R`, `heatmap.R`, `aggregate.R`
- `epigen__rnaseq_pipeline`: `plot_sample_annotation.R`, `annotate_genes.R`
- `maxplanck-ie__snakePipes`: `shared/rscripts/DESeq2.R`
- `sumone-compbio__DGE-Analysis-using-Snakemake-R`: `deseq2.R`, `gsea.R`

### Rejected for missing dependencies
- `EnhancedVolcano` (CRAN install non-trivial on this box): `sumone-compbio__.../volcanoplot.R`, `epigen__dea_limma/volcanos.R`
- `sleuth`: `maxplanck-ie__snakePipes/.../sleuth.R`, `sleuth_allelic.R`
- `wasabi`: `maxplanck-ie__snakePipes/.../wasabi.R`
- `spp` (phantompeakqualtools): `snakemake-workflows__chipseq/run_spp.R`, `phantompeak_correlation.R`, `epigen__300BCG_ATACseq_pipeline/run_spp_nodups.R`
- `monocle`, `RaceID`: `snakePipes/scRNAseq_cell_filter_*.R`, `scRNAseq_select_threshold_cluster_*.R`
- `scater`, `scran`: `snakemake-workflows__single-cell-rna-seq/normalize.R` and siblings
- `Gviz`, `GenomicFeatures`, `rtracklayer`, `txdbmaker`: `joncahn__.../R_browser_plot.R`
- `DMRcaller`: `joncahn__.../R_call_DMRs*.R`
- `ComplexUpset` (plus `remotes::install_github` from the script itself, which we refuse to execute): `joncahn__.../R_Upset_plot_*.R`
- `AnnotationForge`, `rrvgo`, `topGO`: `joncahn__.../R_build_GO_database.R`, `R_GO_analysis.R`
- `biomaRt`, `apeglm`, `clusterProfiler`, `enrichplot`, `org.Mm.eg.db`, `DOSE`: various

### Rejected for hard-coded output paths (outputs not cleanly redirectable)
- `joncahn__.../R_call_DEGs.R` — writes to `results/RNA/DEG/...` and `results/combined/plots/...` with no output-dir argument.
- `joncahn__.../R_sizes_stats.R` — writes to `results/combined/plots/srna_sizes_stats_*.pdf` with no output-dir argument.
- `joncahn__.../R_gene_expression_rpkm.R` — hardcoded `results/RNA/DEG/`.
- `joncahn__.../R_call_srna_DEGs.R` — hardcoded `results/RNA/DEG/`.
- `joncahn__.../R_plot_expression_level.R` — requires a `.RData` object produced by `R_call_DEGs.R`; no output-dir argument and inputs are intermediate artefacts only.
- `gersteinlab__ASTRO/.../STRS/draw_violin_plot.R` — reads intermediate TSVs under `./result/` and removes them at the end; workspace contamination risks flagged behaviour, deferred in favour of the sibling `plot_violin_step3.R`.

### Deferred (technically wrappable but requires extra rigging)
- `gammon-bio__rnaseq_pipeline/scripts/run_deseq2.R` — uses `optparse` + `rmarkdown::render` with a companion `.Rmd`; requires copying / inlining the Rmd, out of scope for this batch.

## Final task_id list

```
akinyi_deseq2
riya_limma
snakepipes_merge_fc
snakepipes_merge_ct
chipseq_plot_peak_intersect
chipseq_plot_macs_qc
chipseq_plot_homer_annot
snakepipes_scrna_merge_coutt
snakepipes_scrna_qc
epigenbutton_mapping_stats
epigenbutton_peak_stats
smartseqtotal_violin
```

## Counts summary

- Candidate R scripts surveyed / classified: 52 (see `tools/candidate_r_scripts.csv`)
- New tasks added in this batch: 8
- Dropped for `snakemake@`-only: ~28
- Dropped for missing packages: ~18
- Dropped for hardcoded output paths: 6
- Deferred (rmarkdown rigging): 1
- Final ready tasks in registry: **12**
