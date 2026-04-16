# Benchmark Release Candidates

更新日期: 2026-04-10

- 已通过 dry-run 的新增 finish workflows: 51
- 首批核心 release 候选: 42
- 扩展候选: 2
- 大型候选: 7

说明:
- `release_core`: 3-40 steps，优先进入首批 benchmark 对比。
- `release_extended`: 2-step 或 过小 workflow，可保留作补充或 sanity check。
- `release_large`: >40 steps 的大型 workflow，适合后续重负载评测。

## Release Core

| Workflow | Steps | Family | 类型 |
|---|---:|---|---|
| `gersteinlab-astro-finish` | 3 | spatial | manual-special |
| `riyadua-cervical-cancer-snakemake-workflow-finish` | 3 | other | auto |
| `saidmlonji-rnaseq_pipeline-finish` | 3 | rna | manual-special |
| `cellranger-count-finish` | 4 | single-cell | auto |
| `gammon-bio-rnaseq_pipeline-finish` | 4 | rna | manual-special |
| `sumone-compbio-dge-analysis-using-snakemake-r-finish` | 4 | other | auto |
| `epigen-fetch_ngs-finish` | 7 | epigenomics | auto |
| `epigen-mixscape_seurat-finish` | 7 | single-cell | auto |
| `akinyi-onyango-rna_seq_pipeline-finish` | 8 | other | auto |
| `lwang-genomics-ngs_pipeline_sn-chip_seq-finish` | 8 | epigenomics | manual-special |
| `star-arriba-fusion-calling-finish` | 8 | rna | auto |
| `lwang-genomics-ngs_pipeline_sn-rna_seq-finish` | 9 | other | manual-special |
| `rna-seq-kallisto-sleuth-finish` | 9 | rna | auto |
| `chandanbfx-scrna-seq-seurat-workflow-finish` | 10 | single-cell | auto |
| `dwheelerau-snakemake-rnaseq-counts-finish` | 10 | rna | auto |
| `epigen-300bcg-atacseq_pipeline-finish` | 10 | epigenomics | manual-special |
| `epigen-dea_seurat-finish` | 10 | single-cell | auto |
| `lwang-genomics-ngs_pipeline_sn-atac_seq-finish` | 10 | epigenomics | manual-special |
| `microsatellite-instability-detection-with-msisensor-pro-finish` | 10 | variant | auto |
| `epigen-dea_limma-finish` | 12 | epigenomics | auto |
| `epigen-genome_tracks-finish` | 12 | epigenomics | auto |
| `cellranger-multi-finish` | 14 | single-cell | auto |
| `epigen-spilterlize_integrate-finish` | 14 | epigenomics | auto |
| `epigen-scrnaseq_processing_seurat-finish` | 15 | single-cell | auto |
| `epigen-enrichment_analysis-finish` | 16 | epigenomics | auto |
| `cite-seq-alevin-fry-seurat-finish` | 18 | single-cell | auto |
| `tgirke-systempiperdata-spscrna-finish` | 18 | single-cell | manual-special |
| `gustaveroussy-sopa-finish` | 20 | spatial | auto |
| `dna-seq-short-read-circle-map-finish` | 21 | variant | auto |
| `tgirke-systempiperdata-chipseq-finish` | 21 | epigenomics | manual-special |
| `tgirke-systempiperdata-rnaseq-finish` | 21 | rna | manual-special |
| `fritjoflammers-snakemake-methylanalysis-finish` | 22 | epigenomics | auto |
| `single-cell-rna-seq-finish` | 22 | single-cell | auto |
| `semenko-serpent-methylation-pipeline-finish` | 24 | epigenomics | auto |
| `epigen-atacseq_pipeline-finish` | 26 | epigenomics | auto |
| `epigen-rnaseq_pipeline-finish` | 26 | epigenomics | auto |
| `epigen-unsupervised_analysis-finish` | 27 | epigenomics | auto |
| `tgirke-systempiperdata-riboseq-finish` | 32 | other | manual-special |
| `cyrcular-calling-finish` | 34 | other | auto |
| `tgirke-systempiperdata-varseq-finish` | 35 | variant | manual-special |
| `read-alignment-pangenome-finish` | 38 | other | auto |
| `maxplanck-ie-snakepipes-finish` | 39 | other | auto |

## Release Extended

| Workflow | Steps | Family | 类型 |
|---|---:|---|---|
| `jfnavarro-st_pipeline-finish` | 2 | spatial | manual-special |
| `mohammedemamkhattabunipd-atacseq-finish` | 2 | epigenomics | manual-special |

## Release Large

| Workflow | Steps | Family | 类型 |
|---|---:|---|---|
| `rna-longseq-de-isoform-finish` | 43 | other | auto |
| `dna-seq-benchmark-finish` | 68 | variant | auto |
| `chipseq-finish` | 70 | epigenomics | auto |
| `single-cell-drop-seq-finish` | 70 | single-cell | auto |
| `dna-seq-neoantigen-prediction-finish` | 79 | variant | auto |
| `joncahn-epigeneticbutton-finish` | 126 | epigenomics | auto |
| `mckellardw-slide_snake-finish` | 146 | spatial | auto |
