---
name: pipeline-rna-seq-star-deseq2-finish
source_type: pipeline
workflow_id: rna-seq-star-deseq2-finish
workflow_dir: main/finish/workflow_candidates/snakemake-workflows__rna-seq-star-deseq2
generated_at: 2026-04-16T16:55:27Z
model: openrouter/openai/gpt-4o
files_used: 21
chars_used: 41966
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method

This pipeline performs differential gene expression analysis using RNA-Seq data. It employs the STAR aligner for mapping reads to a reference genome and DESeq2 for differential expression analysis. The pipeline is designed to handle both single-end and paired-end reads, with optional trimming using fastp. It includes quality control steps using RSeQC and generates a comprehensive report with MultiQC. The pipeline assumes that the input data is either in FASTQ format or accessible via SRA accession numbers. Key steps include alignment with STAR, generation of count matrices, conversion of gene IDs to symbols using biomaRt, and differential expression analysis with DESeq2, including PCA plots for visualization.

## Parameters

- `samples`: Path to the samples TSV file (e.g., `config_basic/samples.tsv`).
- `units`: Path to the units TSV file (e.g., `config_basic/units.tsv`).
- `ref/species`: Species name for reference genome (e.g., `saccharomyces_cerevisiae`).
- `ref/release`: Release version of the reference genome (e.g., `115`).
- `ref/build`: Build version of the reference genome (e.g., `R64-1-1`).
- `trimming/activate`: Boolean to activate trimming (default: `True`).
- `pca/activate`: Boolean to activate PCA analysis (default: `True`).
- `pca/labels`: Labels for PCA plots (e.g., `condition`).
- `diffexp/variables_of_interest`: Variables of interest for differential expression (e.g., `condition` with `base_level: untreated`).
- `diffexp/batch_effects`: Batch effects to consider (default: `""`).
- `diffexp/contrasts`: Contrasts for differential expression (e.g., `treated-vs-untreated`).
- `diffexp/model`: Model formula for DESeq2 (e.g., `~condition`).
- `params/star/index`: Additional parameters for STAR indexing (default: `""`).
- `params/star/align`: Additional parameters for STAR alignment (default: `""`).

## Commands / Code Snippets

```r
# DESeq2 initialization script
library(stringr)
library("DESeq2")

counts_data <- read.table(
  snakemake@input[["counts"]],
  header = TRUE,
  row.names = "gene",
  check.names = FALSE
)

col_data <- read.table(
  snakemake@config[["samples"]],
  header = TRUE,
  row.names = "sample_name",
  check.names = FALSE
)

dds <- DESeqDataSetFromMatrix(
  countData = counts_data,
  colData = col_data,
  design = as.formula(snakemake@config[["diffexp"]][["model"]])
)

dds <- DESeq(dds, parallel = parallel)
saveRDS(dds, file = snakemake@output[[1]])
```

```r
# DESeq2 differential expression script
library("DESeq2")

dds <- readRDS(snakemake@input[[1]])

contrast_config <- snakemake@config[["diffexp"]][["contrasts"]][[
    snakemake@wildcards[["contrast"]]
]]

contrast <- c(
  contrast_config[["variable_of_interest"]],
  contrast_config[["level_of_interest"]],
  snakemake@config[["diffexp"]][["variables_of_interest"]][[
    contrast_config[["variable_of_interest"]]
  ]][["base_level"]]
)

res <- results(
  dds,
  contrast = contrast,
  parallel = parallel
)

res <- lfcShrink(
  dds,
  contrast = contrast,
  res = res,
  type = "ashr"
)

write.table(
  data.frame(
    "gene" = rownames(res),
    res
  ),
  file = snakemake@output[["table"]],
  row.names = FALSE,
  sep = "\t"
)
```

## Notes for R-analysis agent

- The pipeline uses the DESeq2 package for differential expression analysis. Ensure that the `samples.tsv` file contains all necessary metadata columns specified in `config.yaml` under `diffexp: variables_of_interest` and `batch_effects`.
- The STAR aligner requires a pre-built genome index. Ensure that the reference genome and annotation files are correctly specified and available.
- The `gene2symbol.R` script uses biomaRt to convert Ensembl gene IDs to gene symbols. Ensure internet access for biomaRt queries.
- PCA plots are generated using DESeq2's `plotPCA` function. The `intgroup` parameter should match the labels specified in `config.yaml`.
- Check the `fastp` HTML reports for adapter trimming efficiency if automatic detection is used. Adjust `fastp_adapters` and `fastp_extra` settings in `units.tsv` if necessary.
- The pipeline assumes that all samples are either single-end or paired-end, as mixed configurations are not supported.
