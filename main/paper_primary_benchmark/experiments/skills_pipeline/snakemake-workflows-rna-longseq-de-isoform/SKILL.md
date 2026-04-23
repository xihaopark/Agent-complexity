---
name: pipeline-snakemake-workflows-rna-longseq-de-isoform
source_type: pipeline
workflow_id: snakemake-workflows-rna-longseq-de-isoform
workflow_dir: /Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/snakemake-workflows__rna-longseq-de-isoform
generated_at: 2026-04-16T19:32:40Z
model: openrouter/openai/gpt-4o
files_used: 28
chars_used: 80000
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
The pipeline is designed for RNA-seq analysis focusing on long-read sequencing data to perform differential expression (DE) and isoform analysis. It uses a combination of tools and methods to process raw sequencing data, align reads, quantify gene expression, and analyze differential expression at both the gene and isoform levels. The pipeline includes quality control steps, alignment using Minimap2, quantification with Salmon, and differential expression analysis using DESeq2. For isoform analysis, it employs the FLAIR tool to handle splice-isoform analysis. The pipeline also supports protein annotation using the Lambda tool to identify similar proteins based on differentially expressed genes.

## Parameters
- `samples`: Path to the samples CSV file containing sample metadata.
- `inputdir`: Directory where input reads are located.
- `ref.genome`: Path to the reference genome file.
- `ref.annotation`: Path to the annotation file.
- `ref.accession`: NCBI accession number for reference data.
- `ref.ensembl_species`: Ensembl species name for downloading reference data.
- `ref.build`: Genome build version for Ensembl.
- `ref.release`: Ensembl release version.
- `read_filter.min_length`: Minimum read length for filtering (default: 10).
- `minimap2.index_opts`: Options for Minimap2 indexing.
- `minimap2.opts`: Options for Minimap2 mapping.
- `minimap2.maximum_secondary`: Maximum number of secondary alignments (default: 100).
- `minimap2.secondary_score_ratio`: Secondary score ratio for Minimap2 (default: 1.0).
- `samtools.samtobam_opts`: Options for converting SAM to BAM.
- `samtools.bamsort_opts`: Options for sorting BAM files.
- `samtools.bamindex_opts`: Options for indexing BAM files.
- `samtools.bamstats_opts`: Options for generating BAM statistics.
- `quant.salmon_libtype`: Library type for Salmon quantification (default: "U").
- `deseq2.design_factors`: Design factors for DESeq2 normalization.
- `deseq2.batch_effect`: Batch effect factors for DESeq2.
- `deseq2.fit_type`: Fit type for DESeq2 model.
- `deseq2.lfc_null`: Log fold change under the null hypothesis (default: 0).
- `deseq2.alt_hypothesis`: Alternative hypothesis for Wald test (default: "greaterAbs").
- `deseq2.mincount`: Minimum count threshold for DESeq2 (default: 10).
- `deseq2.alpha`: Type I error cutoff value (default: 0.99).
- `deseq2.threshold_plot`: Number of top values to plot in heatmap (default: 10).
- `deseq2.colormap`: Colormap for DESeq2 plots (default: "Blues").
- `isoform_analysis.FLAIR`: Enable FLAIR isoform analysis (default: false).
- `isoform_analysis.qscore`: Minimum MAPQ for isoform assignment (default: 1).
- `isoform_analysis.exp_thresh`: Expression threshold for isoforms (default: 10).
- `isoform_analysis.col_opts`: Options for FLAIR collapse step.
- `protein_annotation.lambda`: Enable Lambda protein annotation (default: true).
- `protein_annotation.uniref`: URL for UniRef database.
- `protein_annotation.num_matches`: Maximum number of protein matches (default: 3).

## Commands / Code Snippets
```r
# DESeq2 initialization script
library("DESeq2")
counts_data <- read.table(snakemake@input[["all_counts"]], header = TRUE, row.names = "Reference", check.names = FALSE)
col_data <- read.table(snakemake@input[["samples"]], header = TRUE, row.names = "sample", check.names = FALSE)
dds <- DESeqDataSetFromMatrix(countData = counts_data, colData = col_data, design = as.formula(design_formula))
dds <- DESeq(dds, parallel = parallel)
saveRDS(dds, file = snakemake@output[[1]])
```

```r
# DESeq2 differential expression analysis
library("DESeq2")
dds <- readRDS(snakemake@input[[1]])
res <- results(dds, contrast = contrast, parallel = parallel, alpha = snakemake@params[["alpha"]], lfcThreshold = as.numeric(snakemake@params[["lfc_null"]]), altHypothesis = snakemake@params[["alt_hypothesis"]])
res <- lfcShrink(dds, contrast = contrast, res = res, type = "ashr")
write.table(data.frame(gene = rownames(res), res), file = snakemake@output[["table"]], row.names = FALSE, sep = "\t", quote = FALSE)
```

```r
# PCA plot generation
library("DESeq2")
dds <- readRDS(snakemake@input[[1]])
counts <- rlog(dds, blind=FALSE)
plotPCA(counts, intgroup = variable)
```

## Notes for R-analysis agent
- The DESeq2 analysis is initialized with `DESeqDataSetFromMatrix` using count data and sample metadata. Ensure that the `samples.csv` file contains the necessary columns specified in `design_factors` and `batch_effect`.
- The pipeline uses `lfcShrink` with the "ashr" method for log fold change shrinkage. Verify that the `lfc_null` and `alt_hypothesis` parameters are set appropriately for the analysis.
- PCA plots are generated using `plotPCA` from the DESeq2 package. Ensure that the variable used for grouping in PCA is present in the colData of the DESeqDataSet.
- The pipeline assumes exactly two conditions for isoform analysis with FLAIR. Check that the `condition` column in `samples.csv` meets this requirement.
- The pipeline uses a specific colormap ("Blues") for heatmaps. Adjust the `colormap` parameter if a different palette is desired.
