---
name: pipeline-epigen-spilterlize_integrate-finish
source_type: pipeline
workflow_id: epigen-spilterlize_integrate-finish
workflow_dir: /Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/epigen__spilterlize_integrate
generated_at: 2026-04-16T19:31:38Z
model: openrouter/openai/gpt-4o
files_used: 20
chars_used: 68023
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
The pipeline is designed to process next-generation sequencing (NGS) count data, such as RNA-seq, ATAC-seq, or ChIP-seq, by performing a series of steps: splitting, filtering, normalizing, integrating, and selecting highly variable features (HVFs). The biological question it addresses is how to preprocess and integrate NGS data to correct for technical biases and unwanted variation while preserving biological signals. The pipeline uses several statistical methods: 

1. **Splitting**: The data is split based on specified metadata columns using Python's pandas library.
2. **Filtering**: Features are filtered using the `filterByExpr` function from the edgeR package in R, which reduces the dataset to features with sufficient expression.
3. **Normalization**: The pipeline supports multiple normalization methods:
   - `CalcNormFactors` from edgeR for TMM, RLE, and other methods.
   - Conditional Quantile Normalization (CQN) using the cqn package.
   - VOOM normalization from the limma package to estimate mean-variance relationships.
4. **Integration**: Batch effects are removed using `removeBatchEffect` from limma, allowing for the integration of data across different conditions or batches.
5. **HVF Selection**: Highly variable features are selected based on normalized dispersion, using methods adapted from Zheng (2017) Nature Communications.
6. **Visualization**: The pipeline includes confounding factor analysis (CFA) and various diagnostic plots to assess the effects of metadata on the data.

## Parameters
- `mem`: Default '8000'. Memory allocation in MB.
- `threads`: Default 1. Number of threads to use.
- `data`: Path to the input count-matrix CSV file.
- `annotation`: Path to the input sample annotation CSV file.
- `result_path`: Path to the output folder.
- `project_name`: Name of the project/dataset.
- `feature_annotation`: Path to the feature annotation CSV file.
- `split_by`: List of metadata columns to split the data by.
- `filter_parameters`: Parameters for edgeR's `filterByExpr` function.
- `edgeR_parameters`: Parameters for edgeR normalization methods.
- `cqn_parameters`: Parameters for CQN normalization.
- `voom_parameters`: Parameters for VOOM normalization.
- `removeBatchEffect_parameters`: Parameters for batch effect removal using limma.
- `hvf_parameters`: Parameters for HVF selection.
- `visualization_parameters`: Metadata columns for visualization.

## Commands / Code Snippets
```r
# Example R code for confounding factor analysis
library("ggplot2")
library("reshape2")
library("data.table")

annot_path <- snakemake@input[["annotation"]]
plot_path <- snakemake@output[["cfa_plot"]]
cfa_results_path <- snakemake@output[["cfa_results"]]

annot <- data.frame(fread(file.path(annot_path), header=TRUE), row.names=1, check.names=FALSE)

# Perform pairwise statistical association testing
p_values <- data.frame(var1=character(), var2=character(), p_value=numeric(), stringsAsFactors=FALSE)
var_names <- colnames(annot)

for(i in 1:(length(var_names)-1)){
  for(j in (i+1):length(var_names)){
    x <- annot[[var_names[i]]]
    y <- annot[[var_names[j]]]
    type_x <- if(is.numeric(x)) "numeric" else "categorical"
    type_y <- if(is.numeric(y)) "numeric" else "categorical"
    
    if(type_x=="numeric" && type_y=="numeric"){
        pvalue <- cor.test(x, y, method="kendall")$p.value
    } else if(type_x=="categorical" && type_y=="categorical"){
        pvalue <- fisher.test(table(x, y), simulate.p.value=TRUE, B=10000)$p.value
    } else {
      if(type_x=="numeric"){
        pvalue <- kruskal.test(x ~ as.factor(y))$p.value
      } else {
        pvalue <- kruskal.test(y ~ as.factor(x))$p.value
      }
    }
    p_values <- rbind(p_values, data.frame(var1=var_names[i], var2=var_names[j], p_value=pvalue, stringsAsFactors=FALSE))
  }
}

# Adjust p-values for multiple testing
p_values$p_values_adjusted <- p.adjust(as.vector(p_values$p_value), method = "BH")

# Plot
cfa_plot <- ggplot(df_long, aes(x=Var1, y=Var2, fill=log_p)) +
    geom_tile(color="black") +
    scale_fill_gradient2(low = "royalblue4", high = "firebrick2", mid = "white", midpoint = 0, name = "") +
    labs(title = "Pairwise statistical association between metadata as -log10 adjusted P-values", x="", y="") +
    theme_minimal(base_size = 10) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1),
       plot.title = element_text(size = 8),
        legend.position = "none")

ggsave(plot_path, cfa_plot, width=heigth_hm, height=heigth_hm, dpi = 300)
write.csv(df_long, file=cfa_results_path, row.names=TRUE)
```

## Notes for R-analysis agent
- **R Packages**: The pipeline uses edgeR for filtering and normalization, limma for batch effect removal and VOOM normalization, and cqn for conditional quantile normalization.
- **Input Shapes**: Expect input count matrices to be in CSV format with features as rows and samples as columns. Annotation files should have samples as rows and metadata as columns.
- **Normalization Choices**: Ensure the correct normalization method is selected based on the config file. Check if feature annotation is provided for RPKM and CQN methods.
- **Metadata Columns**: Verify that the metadata columns specified for splitting and visualization exist in the annotation file.
- **Batch Effect Removal**: Confirm that the desired and unwanted effects for batch correction are correctly specified and present in the annotation data.
- **Visualization**: Check that the metadata columns used for visualization are correctly specified and available in the annotation data.
