# R Workflow Candidate Pool

更新日期: 2026-04-10

目的:
- 先把可扩展进 benchmark 的 R workflow 候选池堆到数量下限。
- 本文件当前不做难度分级、不判断是否含分支、不判断最终是否保留。
- 只记录当前检索到的公开 workflow / pipeline / template 候选，方便后续继续筛选与接入。
- 当前列表已尽量排除“单脚本 / 单步骤 R code”形式的条目，只保留明显是多步骤 workflow / pipeline 的候选。

纳入原则:
- 优先收录带有明显 R 分析核心的 workflow。
- 优先收录可迁移到现有 `finish` 结构的仓库: 有独立 workflow、配置、输入表、可拆步执行的 pipeline。
- 允许混合来源: Snakemake workflow、R-native workflow template、以 R 为核心的数据分析 pipeline。

## 当前候选数

- 当前已收集候选: 53
- 其中包含:
- Snakemake-Workflows 组织仓库
- epigen / MrBiomics 系列仓库
- systemPipeR / systemPipeRdata 工作流模板
- 独立 GitHub R pipeline / Snakemake + R 仓库

## 候选清单

| # | 名称 | 类型 | R 相关性 | 来源 |
|---|---|---|---|---|
| 1 | `snakemake-workflows/rna-seq-star-deseq2` | Snakemake workflow | DESeq2 | https://github.com/snakemake-workflows/rna-seq-star-deseq2 |
| 2 | `snakemake-workflows/rna-seq-kallisto-sleuth` | Snakemake workflow | sleuth | https://github.com/snakemake-workflows/rna-seq-kallisto-sleuth |
| 3 | `snakemake-workflows/single-cell-rna-seq` | Snakemake workflow | 单细胞 DE / cell type assignment | https://github.com/snakemake-workflows/single-cell-rna-seq |
| 4 | `snakemake-workflows/cite-seq-alevin-fry-seurat` | Snakemake workflow | Seurat | https://github.com/snakemake-workflows/cite-seq-alevin-fry-seurat |
| 5 | `snakemake-workflows/rna-longseq-de-isoform` | Snakemake workflow | 长读长 DE / isoform | https://github.com/snakemake-workflows/rna-longseq-de-isoform |
| 6 | `snakemake-workflows/single-cell-drop-seq` | Snakemake workflow | scRNA-seq preprocessing | https://github.com/snakemake-workflows/single-cell-drop-seq |
| 7 | `snakemake-workflows/cellranger-count` | Snakemake workflow | scRNA-seq counting | https://github.com/snakemake-workflows/cellranger-count |
| 8 | `snakemake-workflows/cellranger-multi` | Snakemake workflow | scRNA-seq preprocessing | https://github.com/snakemake-workflows/cellranger-multi |
| 9 | `epigen/scrnaseq_processing_seurat` | Snakemake workflow | Seurat | https://github.com/epigen/scrnaseq_processing_seurat |
| 10 | `epigen/dea_seurat` | Snakemake workflow | Seurat differential expression | https://github.com/epigen/dea_seurat |
| 11 | `epigen/dea_limma` | Snakemake workflow | limma | https://github.com/epigen/dea_limma |
| 12 | `epigen/mixscape_seurat` | Snakemake workflow | Seurat Mixscape | https://github.com/epigen/mixscape_seurat |
| 13 | `epigen/spilterlize_integrate` | Snakemake workflow | 归一化 / integration / HVF | https://github.com/epigen/spilterlize_integrate |
| 14 | `epigen/rnaseq_pipeline` | Snakemake workflow | RNA-seq 处理与注释 | https://github.com/epigen/rnaseq_pipeline |
| 15 | `epigen/atacseq_pipeline` | Snakemake workflow | ATAC-seq quantification / annotation | https://github.com/epigen/atacseq_pipeline |
| 16 | `epigen/enrichment_analysis` | Snakemake workflow | enrichment analysis | https://github.com/epigen/enrichment_analysis |
| 17 | `epigen/unsupervised_analysis` | Snakemake workflow | 降维 / clustering / 可视化 | https://github.com/epigen/unsupervised_analysis |
| 18 | `dwheelerau/snakemake-rnaseq-counts` | Snakemake workflow | RNA-seq counts | https://github.com/dwheelerau/snakemake-rnaseq-counts |
| 19 | `sumone-compbio/DGE-Analysis-using-Snakemake-R` | Snakemake + R | DESeq2 / volcano / GSEA | https://github.com/sumone-compbio/DGE-Analysis-using-Snakemake-R |
| 20 | `RiyaDua/cervical-cancer-snakemake-workflow` | Snakemake + R | gene expression / DE / visualization | https://github.com/RiyaDua/cervical-cancer-snakemake-workflow |
| 21 | `saidmlonji/rnaseq_pipeline` | R/Bash pipeline | Bioconductor / DESeq2 / Gviz | https://github.com/saidmlonji/rnaseq_pipeline |
| 22 | `gammon-bio/rnaseq_pipeline` | RNA-seq pipeline | RNA-seq pipeline | https://github.com/gammon-bio/rnaseq_pipeline |
| 23 | `chandanbfx/scRNA-seq-Seurat-Workflow` | R workflow | Seurat | https://github.com/chandanbfx/scRNA-seq-Seurat-Workflow |
| 24 | `mohammedemamkhattabunipd/ATACseq` | R workflow | Signac / scATAC | https://github.com/mohammedemamkhattabunipd/ATACseq |
| 25 | `joncahn/epigeneticbutton` | Snakemake workflow | integrative chromatin characterization | https://github.com/joncahn/epigeneticbutton |
| 26 | `systemPipeRdata rnaseq` | R workflow template | RNA-Seq | https://bioconductor.org/packages/release/data/experiment/html/systemPipeRdata.html |
| 27 | `systemPipeRdata chipseq` | R workflow template | ChIP-Seq | https://girke.bioinformatics.ucr.edu/GEN242/tutorials/spchipseq/spchipseq/ |
| 28 | `systemPipeRdata riboseq` | R workflow template | RIBO-Seq | https://bioconductor.org/packages/release/data/experiment/html/systemPipeRdata.html |
| 29 | `systemPipeRdata varseq` | R workflow template | VARseq | https://systempipe.org/spr_wf/installwf/ |
| 30 | `systemPipeRdata scrna` | R workflow template | scRNA-Seq / Seurat | https://bioconductor.org/packages/release/data/experiment/html/systemPipeRdata.html |
| 31 | `rseqR` | R pipeline framework | DESeq2 / edgeR / limma-voom | https://anilchalisey.github.io/rseqR/ |
| 32 | `Transcriptomic RNA-seq Pipeline` | R pipeline | DESeq2 / limma / clusterProfiler / fgsea | https://akhileshkaushal.github.io/transcriptomic/index.html |
| 33 | `slide_snake` | Snakemake workflow | spatial RNA-seq | https://github.com/mckellardw/slide_snake |
| 34 | `ASTRO` | workflow pipeline | spatial whole-transcriptome RNA-expression | https://github.com/gersteinlab/ASTRO |
| 35 | `semenko/serpent-methylation-pipeline` | Snakemake workflow | methylation analysis | https://github.com/semenko/serpent-methylation-pipeline |
| 36 | `snakemake-workflows/chipseq` | Snakemake workflow | ChIP-seq differential analysis | https://github.com/snakemake-workflows/chipseq |
| 37 | `snakemake-workflows/star-arriba-fusion-calling` | Snakemake workflow | RNA-seq / fusion calling | https://github.com/snakemake-workflows/star-arriba-fusion-calling |
| 38 | `snakemake-workflows/read-alignment-pangenome` | Snakemake workflow | read alignment / pangenome | https://github.com/snakemake-workflows/read-alignment-pangenome |
| 39 | `snakemake-workflows/dna-seq-benchmark` | Snakemake workflow | variant benchmarking | https://github.com/snakemake-workflows/dna-seq-benchmark |
| 40 | `snakemake-workflows/dna-seq-neoantigen-prediction` | Snakemake workflow | neoantigen prediction | https://github.com/snakemake-workflows/dna-seq-neoantigen-prediction |
| 41 | `snakemake-workflows/microsatellite-instability-detection-with-msisensor-pro` | Snakemake workflow | MSI detection | https://github.com/snakemake-workflows/microsatellite-instability-detection-with-msisensor-pro |
| 42 | `snakemake-workflows/cyrcular-calling` | Snakemake workflow | ecDNA calling | https://github.com/snakemake-workflows/cyrcular-calling |
| 43 | `snakemake-workflows/dna-seq-short-read-circle-map` | Snakemake workflow | circle DNA calling | https://github.com/snakemake-workflows/dna-seq-short-read-circle-map |
| 44 | `snakemake-workflows/oncology` | Snakemake workflow | oncology cohort studies | https://github.com/snakemake-workflows/oncology |
| 45 | `maxplanck-ie/snakePipes` | Snakemake workflow suite | epigenomics / RNA-seq / ChIP-seq / ATAC-seq | https://github.com/maxplanck-ie/snakePipes |
| 46 | `lwang-genomics/NGS_pipeline_sn` | Snakemake workflow | RNA-seq / ChIP-seq / ATAC-seq | https://github.com/lwang-genomics/NGS_pipeline_sn |
| 47 | `Akinyi-Onyango/rna_seq_pipeline` | Snakemake workflow | RNA-seq DE pipeline | https://github.com/Akinyi-Onyango/rna_seq_pipeline |
| 48 | `fritjoflammers/snakemake-methylanalysis` | Snakemake workflow | methylkit analysis | https://github.com/fritjoflammers/snakemake-methylanalysis |
| 49 | `jfnavarro/st_pipeline` | spatial transcriptomics workflow | ST / Visium pipeline | https://github.com/jfnavarro/st_pipeline |
| 50 | `gustaveroussy/sopa` | Snakemake workflow | spatial omics analysis | https://github.com/gustaveroussy/sopa |
| 51 | `epigen/fetch_ngs` | Snakemake workflow | public sequencing data + metadata fetching | https://github.com/epigen/fetch_ngs |
| 52 | `epigen/genome_tracks` | Snakemake workflow | genome browser track generation | https://github.com/epigen/genome_tracks |
| 53 | `epigen/300BCG_ATACseq_pipeline` | Snakemake workflow | ATAC-seq pipeline | https://github.com/epigen/300BCG_ATACseq_pipeline |

## 备注

- 上述 35 个候选尚未完成:
- 是否能直接运行
- 是否适合拆成 `finish` 风格的 retained steps
- 是否需要额外大体量参考数据
- 是否含自然分支 / 条件分支
- license 与维护状态是否适合长期 benchmark

- 但从“先把数量收上来”的角度，这个候选池已经超过 50 的目标下限。

## 下一步建议

- 对这 35 个候选做第一轮去重:
- 合并同一分析族但仅实现不同的 repo
- 去掉明显太轻量或太 demo 化的仓库
- 优先保留:
- 有独立 `workflow/` 目录或明确 step/rule 结构的仓库
- 有 `samples.tsv` / `config.yaml` / `Snakefile` 等标准入口的仓库
- R 分析核心明确的仓库

- 之后再做第二轮:
- 判断哪些最容易转成你们现有的 `finish` benchmark 格式
- 判断哪些天然有多分支 / 多路径执行潜力
