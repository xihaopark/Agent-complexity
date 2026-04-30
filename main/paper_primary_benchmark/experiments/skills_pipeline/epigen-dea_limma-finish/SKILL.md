---
name: pipeline-epigen-dea_limma-finish
source_type: pipeline
workflow_id: epigen-dea_limma-finish
workflow_dir: /Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/epigen__dea_limma
generated_at: 2026-04-16T19:31:09Z
model: openrouter/openai/gpt-4o
files_used: 16
chars_used: 80000
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
The pipeline performs differential expression analysis (DEA) using the R package `limma`, which is designed for analyzing gene expression data. The workflow is implemented in Snakemake and is capable of handling various types of NGS data, such as RNA-seq, ATAC-seq, and ChIP-seq. The analysis involves fitting a linear model to the data to identify features (genes or regions) that show statistically significant changes between conditions. The pipeline supports optional steps such as normalization using `edgeR::calcNormFactors`, variance modeling with `voom`, and empirical Bayes moderation with `eBayes`. Additionally, it can perform one-vs-all (OvA) analyses to identify group-specific signatures by comparing each group against all others combined. Visualization of results is achieved through volcano plots, heatmaps, and bar plots, using R packages like `EnhancedVolcano`, `pheatmap`, and `ggplot2`.

## Parameters
- `mem`: Default is '32000'. Memory allocation for the workflow.
- `threads`: Default is 1. Number of threads to use.
- `annotation`: Path to the annotation CSV file.
- `feature_annotation`: Path to the feature annotation file and the column name for alternative feature names.
- `result_path`: Path to the directory where results will be stored.
- `project_name`: Name of the project or dataset.
- `reference_levels`: Reference levels for variables of interest, e.g., treatment and time.
- `score_formula`: Formula for calculating feature scores, default is "-log10(dea_results$P.Value)*sign(dea_results$logFC)".
- `filters`: Criteria for filtering DEA results, including `adj_pval` (default 0.05), `lfc` (default 2), and `ave_expr` (default 0).
- `volcano`: Parameters for volcano plots, including `pCutoff` (default 0.05) and `FCcutoff` (default 2).
- `feature_lists`: Paths to feature list files for highlighting in plots.

## Commands / Code Snippets
```r
# Load libraries & utility function
library("limma")
library("edgeR")
library("statmod")
library("data.table")

# Load data
data <- data.frame(fread(file.path(data_path), header=TRUE), row.names=1)
metadata <- data.frame(fread(file.path(metadata_path), header=TRUE, na.strings=c("NA", "")), row.names=1)

# Prepare DEA
model_matrix <- model.matrix(design, metadata)
dge <- DGEList(data, samples=metadata, genes=rownames(data))
dge <- calcNormFactors(dge, method=calcNormFactors_method)
v <- voom(dge, model_matrix, plot=TRUE)

# Fit linear model
lmfit <- lmFit(v, model_matrix)
lmfit <- eBayes(lmfit, robust=TRUE, trend=limma_trend)

# Extract results
dea_results <- topTable(lmfit, coef=coefx, number=nrow(data), sort.by="P")
```

## Notes for R-analysis agent
- The pipeline uses `limma` for DEA, with optional steps for normalization (`edgeR::calcNormFactors`), variance modeling (`voom`), and empirical Bayes moderation (`eBayes`).
- Input data should be a feature-by-sample matrix with features as rows and samples as columns. Metadata should match sample names.
- Ensure the design matrix is full rank to avoid identifiability issues.
- Check the configuration for parameters like `reference_levels`, `score_formula`, and `filters` to ensure they align with the analysis goals.
- Visualization steps use `EnhancedVolcano` for volcano plots and `pheatmap` for heatmaps. Adjust plot parameters as needed for clarity.
- Be cautious with interaction terms in the formula, as they can affect the interpretation of OvA results.
