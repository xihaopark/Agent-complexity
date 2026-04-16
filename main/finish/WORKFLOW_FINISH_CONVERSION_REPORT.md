# Workflow Finish Conversion Report

更新日期: 2026-04-10

- 候选仓库总数: 47
- 已自动转化为 finish workflow: 38
- 当前无法自动转化: 9
- 已完成 dry-run 验证: 38

## 已自动转化并验证

| 源仓库 | 生成目录 | Step 数 | Dry-run 状态 |
|---|---|---:|---|
| `Akinyi-Onyango__rna_seq_pipeline` | `akinyi-onyango-rna_seq_pipeline-finish` | 8 | passed |
| `chandanbfx__scRNA-seq-Seurat-Workflow` | `chandanbfx-scrna-seq-seurat-workflow-finish` | 10 | passed |
| `dwheelerau__snakemake-rnaseq-counts` | `dwheelerau-snakemake-rnaseq-counts-finish` | 10 | passed |
| `epigen__atacseq_pipeline` | `epigen-atacseq_pipeline-finish` | 26 | passed |
| `epigen__dea_limma` | `epigen-dea_limma-finish` | 12 | passed |
| `epigen__dea_seurat` | `epigen-dea_seurat-finish` | 10 | passed |
| `epigen__enrichment_analysis` | `epigen-enrichment_analysis-finish` | 16 | passed |
| `epigen__fetch_ngs` | `epigen-fetch_ngs-finish` | 7 | passed |
| `epigen__genome_tracks` | `epigen-genome_tracks-finish` | 12 | passed |
| `epigen__mixscape_seurat` | `epigen-mixscape_seurat-finish` | 7 | passed |
| `epigen__rnaseq_pipeline` | `epigen-rnaseq_pipeline-finish` | 26 | passed |
| `epigen__scrnaseq_processing_seurat` | `epigen-scrnaseq_processing_seurat-finish` | 15 | passed |
| `epigen__spilterlize_integrate` | `epigen-spilterlize_integrate-finish` | 14 | passed |
| `epigen__unsupervised_analysis` | `epigen-unsupervised_analysis-finish` | 27 | passed |
| `fritjoflammers__snakemake-methylanalysis` | `fritjoflammers-snakemake-methylanalysis-finish` | 22 | passed |
| `gustaveroussy__sopa` | `gustaveroussy-sopa-finish` | 20 | passed |
| `joncahn__epigeneticbutton` | `joncahn-epigeneticbutton-finish` | 126 | passed |
| `maxplanck-ie__snakePipes` | `maxplanck-ie-snakepipes-finish` | 39 | passed |
| `mckellardw__slide_snake` | `mckellardw-slide_snake-finish` | 146 | passed |
| `RiyaDua__cervical-cancer-snakemake-workflow` | `riyadua-cervical-cancer-snakemake-workflow-finish` | 3 | passed |
| `semenko__serpent-methylation-pipeline` | `semenko-serpent-methylation-pipeline-finish` | 24 | passed |
| `snakemake-workflows__cellranger-count` | `cellranger-count-finish` | 4 | passed |
| `snakemake-workflows__cellranger-multi` | `cellranger-multi-finish` | 14 | passed |
| `snakemake-workflows__chipseq` | `chipseq-finish` | 70 | passed |
| `snakemake-workflows__cite-seq-alevin-fry-seurat` | `cite-seq-alevin-fry-seurat-finish` | 18 | passed |
| `snakemake-workflows__cyrcular-calling` | `cyrcular-calling-finish` | 34 | passed |
| `snakemake-workflows__dna-seq-benchmark` | `dna-seq-benchmark-finish` | 68 | passed |
| `snakemake-workflows__dna-seq-neoantigen-prediction` | `dna-seq-neoantigen-prediction-finish` | 79 | passed |
| `snakemake-workflows__dna-seq-short-read-circle-map` | `dna-seq-short-read-circle-map-finish` | 21 | passed |
| `snakemake-workflows__microsatellite-instability-detection-with-msisensor-pro` | `microsatellite-instability-detection-with-msisensor-pro-finish` | 10 | passed |
| `snakemake-workflows__read-alignment-pangenome` | `read-alignment-pangenome-finish` | 38 | passed |
| `snakemake-workflows__rna-longseq-de-isoform` | `rna-longseq-de-isoform-finish` | 43 | passed |
| `snakemake-workflows__rna-seq-kallisto-sleuth` | `rna-seq-kallisto-sleuth-finish` | 74 | passed |
| `snakemake-workflows__rna-seq-star-deseq2` | `rna-seq-star-deseq2-finish` | 25 | passed |
| `snakemake-workflows__single-cell-drop-seq` | `single-cell-drop-seq-finish` | 70 | passed |
| `snakemake-workflows__single-cell-rna-seq` | `single-cell-rna-seq-finish` | 22 | passed |
| `snakemake-workflows__star-arriba-fusion-calling` | `star-arriba-fusion-calling-finish` | 8 | passed |
| `sumone-compbio__DGE-Analysis-using-Snakemake-R` | `sumone-compbio-dge-analysis-using-snakemake-r-finish` | 4 | passed |

## 当前未自动转化

| 源仓库 | 原因 |
|---|---|
| `epigen__300BCG_ATACseq_pipeline` | `no_supported_snakemake_entry` |
| `gammon-bio__rnaseq_pipeline` | `no_supported_snakemake_entry` |
| `gersteinlab__ASTRO` | `no_supported_snakemake_entry` |
| `jfnavarro__st_pipeline` | `no_supported_snakemake_entry` |
| `lwang-genomics__NGS_pipeline_sn` | `no_supported_snakemake_entry` |
| `mohammedemamkhattabunipd__ATACseq` | `no_supported_snakemake_entry` |
| `saidmlonji__rnaseq_pipeline` | `no_supported_snakemake_entry` |
| `snakemake-workflows__oncology` | `no_supported_snakemake_entry` |
| `tgirke__systemPipeRdata` | `no_supported_snakemake_entry` |

## 关键文件

- 候选清单: `finish/R_WORKFLOW_CANDIDATES.md`
- 候选接入报告: `finish/WORKFLOW_CANDIDATE_INTAKE_REPORT.md`
- 自动转化脚本: `finish/tools/auto_finishify_candidates.py`
- 验证结果 JSON: `finish/GENERATED_FINISH_VALIDATION.json`
- 验证结果 Markdown: `finish/GENERATED_FINISH_VALIDATION.md`
