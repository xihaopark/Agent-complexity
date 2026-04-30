---
name: pipeline-RiyaDua-cervical-cancer-snakemake-workflow
source_type: pipeline
workflow_id: RiyaDua-cervical-cancer-snakemake-workflow
workflow_dir: /Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/RiyaDua__cervical-cancer-snakemake-workflow
generated_at: 2026-04-16T19:31:00Z
model: openrouter/openai/gpt-4o
files_used: 5
chars_used: 6785
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
This pipeline is designed to analyze cervical cancer gene expression data from the GEO database. It automates the process of fetching, preprocessing, and analyzing differential gene expression using a Snakemake workflow. The pipeline specifically uses the limma package for differential expression analysis, comparing cancer samples to normal tissue samples. The analysis includes generating a volcano plot to visualize differentially expressed genes. The pipeline is adaptable to multiple cancer types by grouping all cancer samples together versus normal tissue.

## Parameters
- `geo_id`: Default is `"GSE63678"`. This is the GEO Series ID from which the data will be fetched.
- `min_count`: Default is `10`. This parameter sets the minimum count threshold for filtering genes during preprocessing.

## Commands / Code Snippets
```r
# Preprocessing script (preprocessing.R)
geo_id <- Sys.getenv("GEO_ID", "GSE63678")
min_count <- as.numeric(Sys.getenv("MIN_COUNT", "10"))

library(GEOquery)
library(dplyr)
library(tidyr)

gse <- getGEO(geo_id)[[1]]
sampleInfo <- pData(gse)
sampleInfo$group <- ifelse(grepl("normal", sampleInfo$source_name_ch1, ignore.case=TRUE), "normal", "cancer")
exprs_data <- exprs(gse)
exprs_data <- log2(exprs_data + 1)
filtered <- exprs_data[rowSums(exprs_data) > min_count, ]
write.csv(exprs_data, "data/processed_expression_data.csv", row.names=TRUE)
write.csv(sampleInfo, "data/sample_metadata.csv", row.names=TRUE)
```

```r
# Differential expression script (differential_expression.R)
library(DESeq2)
library(limma)
library(ggplot2)
library(pheatmap)

args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
metadata_file <- args[2]
output_file <- args[3]
volcano_plot <- args[4]

exprs_data <- read.csv(input_file, row.names=1)
sample_info <- read.csv(metadata_file, row.names=1)

group <- factor(sample_info$group)
design <- model.matrix(~0 + group)
colnames(design) <- levels(group)

fit <- lmFit(exprs_data, design)
contrasts <- makeContrasts(cancer - normal, levels=design)
fit2 <- contrasts.fit(fit, contrasts)
fit2 <- eBayes(fit2)

deg_results <- topTable(fit2, adjust="fdr", number=250)
write.csv(deg_results, output_file)

if (!is.na(volcano_plot)) {
  p <- ggplot(deg_results, aes(x=logFC, y=-log10(P.Value))) +
    geom_point(alpha=0.6) +
    theme_minimal() +
    labs(title="Volcano Plot", x="Log2 Fold Change", y="-Log10 P-value")
  ggsave(volcano_plot, plot=p)
}
```

## Notes for R-analysis agent
- The pipeline uses the `GEOquery` package to fetch data from GEO and `limma` for differential expression analysis.
- Ensure that the `group` column in the metadata correctly distinguishes between "cancer" and "normal" samples based on the `source_name_ch1` field.
- The `exprs_data` is log2-transformed and filtered based on `min_count`; ensure this preprocessing step is consistent with the analysis goals.
- The `makeContrasts` function in limma is used to define the comparison between "cancer" and "normal" groups; verify that these levels are correctly set in the design matrix.
- The volcano plot is generated using `ggplot2`; ensure the plot is saved correctly to the specified output path.
- The pipeline is designed to run in a conda environment, which includes all necessary R and Bioconductor packages. Ensure this environment is activated before running the scripts.
