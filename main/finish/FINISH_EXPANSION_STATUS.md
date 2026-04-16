# Finish Expansion Status

更新日期: 2026-04-10

- 自动转化 workflow 数: 43
- 特殊定制转化 workflow 数: 14
- 当前 finish workflow 总数: 57
- 当前已覆盖源仓库数: 46
- 当前剩余未完成源仓库数: 1

## 已验证 workflow

| Workflow | Status | Steps | 类型 |
|---|---|---:|---|
| `akinyi-onyango-rna_seq_pipeline-finish` | passed | 8 | auto |
| `cellranger-count-finish` | passed | 4 | auto |
| `cellranger-multi-finish` | passed | 14 | auto |
| `chandanbfx-scrna-seq-seurat-workflow-finish` | passed | 10 | auto |
| `chipseq-finish` | passed | 70 | auto |
| `cite-seq-alevin-fry-seurat-finish` | passed | 18 | auto |
| `cyrcular-calling-finish` | passed | 34 | auto |
| `dna-seq-benchmark-finish` | passed | 68 | auto |
| `dna-seq-neoantigen-prediction-finish` | passed | 79 | auto |
| `dna-seq-short-read-circle-map-finish` | passed | 21 | auto |
| `dwheelerau-snakemake-rnaseq-counts-finish` | passed | 10 | auto |
| `epigen-300bcg-atacseq_pipeline-finish` | passed | 10 | manual-special |
| `epigen-atacseq_pipeline-finish` | passed | 26 | auto |
| `epigen-dea_limma-finish` | passed | 12 | auto |
| `epigen-dea_seurat-finish` | passed | 10 | auto |
| `epigen-enrichment_analysis-finish` | passed | 16 | auto |
| `epigen-fetch_ngs-finish` | passed | 7 | auto |
| `epigen-genome_tracks-finish` | passed | 12 | auto |
| `epigen-mixscape_seurat-finish` | passed | 7 | auto |
| `epigen-rnaseq_pipeline-finish` | passed | 26 | auto |
| `epigen-scrnaseq_processing_seurat-finish` | passed | 15 | auto |
| `epigen-spilterlize_integrate-finish` | passed | 14 | auto |
| `epigen-unsupervised_analysis-finish` | passed | 27 | auto |
| `fritjoflammers-snakemake-methylanalysis-finish` | passed | 22 | auto |
| `gammon-bio-rnaseq_pipeline-finish` | passed | 4 | manual-special |
| `gammon-bio-rnaseq_pipeline-finish` | passed | 4 | manual-special |
| `gersteinlab-astro-finish` | passed | 3 | manual-special |
| `gersteinlab-astro-finish` | passed | 3 | manual-special |
| `gustaveroussy-sopa-finish` | passed | 20 | auto |
| `jfnavarro-st_pipeline-finish` | passed | 2 | manual-special |
| `jfnavarro-st_pipeline-finish` | passed | 2 | manual-special |
| `joncahn-epigeneticbutton-finish` | passed | 126 | auto |
| `lwang-genomics-ngs_pipeline_sn-atac_seq-finish` | passed | 10 | manual-special |
| `lwang-genomics-ngs_pipeline_sn-chip_seq-finish` | passed | 8 | manual-special |
| `lwang-genomics-ngs_pipeline_sn-rna_seq-finish` | passed | 9 | manual-special |
| `maxplanck-ie-snakepipes-finish` | passed | 39 | auto |
| `mckellardw-slide_snake-finish` | passed | 146 | auto |
| `microsatellite-instability-detection-with-msisensor-pro-finish` | passed | 10 | auto |
| `mohammedemamkhattabunipd-atacseq-finish` | passed | 2 | manual-special |
| `mohammedemamkhattabunipd-atacseq-finish` | passed | 2 | manual-special |
| `read-alignment-pangenome-finish` | passed | 38 | auto |
| `riyadua-cervical-cancer-snakemake-workflow-finish` | passed | 3 | auto |
| `rna-longseq-de-isoform-finish` | passed | 43 | auto |
| `rna-seq-kallisto-sleuth-finish` | passed | 9 | auto |
| `rna-seq-star-deseq2-finish` | failed | 7 | auto |
| `saidmlonji-rnaseq_pipeline-finish` | passed | 3 | manual-special |
| `saidmlonji-rnaseq_pipeline-finish` | passed | 3 | manual-special |
| `semenko-serpent-methylation-pipeline-finish` | passed | 24 | auto |
| `single-cell-drop-seq-finish` | passed | 70 | auto |
| `single-cell-rna-seq-finish` | passed | 22 | auto |
| `star-arriba-fusion-calling-finish` | passed | 8 | auto |
| `sumone-compbio-dge-analysis-using-snakemake-r-finish` | passed | 4 | auto |
| `tgirke-systempiperdata-chipseq-finish` | passed | 21 | manual-special |
| `tgirke-systempiperdata-riboseq-finish` | passed | 32 | manual-special |
| `tgirke-systempiperdata-rnaseq-finish` | passed | 21 | manual-special |
| `tgirke-systempiperdata-spscrna-finish` | passed | 18 | manual-special |
| `tgirke-systempiperdata-varseq-finish` | passed | 35 | manual-special |

## 当前未完成源仓库

| 源仓库 | 说明 |
|---|---|
| `snakemake-workflows__oncology` | 上游仓库当前只有 README，没有可执行 workflow 资产，无法有意义地 finish 化。 |

## 关键文件

- 自动转化脚本: `finish/tools/auto_finishify_candidates.py`
- 特殊定制转化脚本: `finish/tools/manual_finishify_specials.py`
- 统一入口脚本: `finish/tools/finishify_workflows.py`
- 自动验证: `finish/GENERATED_FINISH_VALIDATION.md`
- 特殊验证: `finish/MANUAL_FINISH_VALIDATION.md`
- 状态 JSON: `finish/FINISH_EXPANSION_STATUS.json`
