---
name: pipeline-snakemake-workflows-chipseq-finish
source_type: pipeline
workflow_id: snakemake-workflows-chipseq-finish
workflow_dir: /Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/snakemake-workflows__chipseq
generated_at: 2026-04-16T19:32:24Z
model: openrouter/openai/gpt-4o
files_used: 21
chars_used: 80000
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
This pipeline is designed for ChIP-seq data analysis, focusing on peak calling and downstream analysis. It uses a combination of tools and methods to process raw sequencing data, perform quality control, map reads to a reference genome, call peaks, and conduct differential analysis. Key steps include:

1. **Quality Control and Trimming**: Uses FastQC for initial quality checks and Cutadapt for trimming adapters from raw FASTQ files.
2. **Mapping**: Aligns reads to a reference genome using BWA, followed by sorting and filtering with Samtools and Bamtools.
3. **Peak Calling**: Utilizes MACS2 for both broad and narrow peak calling, with options for handling single-end or paired-end data.
4. **Consensus Peak Analysis**: Merges peaks across samples using Bedtools and performs annotation with HOMER.
5. **Differential Analysis**: Conducts differential binding analysis using featureCounts and DESeq2, generating PCA and heatmap plots for visualization.
6. **Post-Analysis**: Includes additional quality metrics and visualization using tools like deepTools and PhantomPeakQualTools.

The pipeline assumes the availability of a reference genome and annotation files, and it can handle both single-end and paired-end data. It also supports the use of control samples for peak calling.

## Parameters
- `single_end`: Boolean, indicates if the data is single-end.
- `resources.ref.build`: String, reference genome build.
- `resources.ref.chromosome`: String, specific chromosome to analyze.
- `params.peak-analysis`: String, type of peak analysis ('narrow' or 'broad').
- `params.min-reps-consensus`: Integer, minimum replicates for consensus peaks.
- `params.cutadapt-pe`: String, parameters for paired-end adapter trimming.
- `params.cutadapt-se`: String, parameters for single-end adapter trimming.
- `params.cutadapt-others`: String, additional Cutadapt parameters.
- `params.callpeak.p-value`: Float, p-value threshold for MACS2.
- `params.callpeak.q-value`: Float, q-value threshold for MACS2.

## Commands / Code Snippets
```r
# DESeq2 analysis and plotting
library(DESeq2)
library(vsn)
library(ggplot2)
library(RColorBrewer)
library(pheatmap)
library(lattice)
library(BiocParallel)

featurecount_file <- snakemake@input[[1]]
count.table <- read.delim(file=featurecount_file, header=TRUE)
rownames(count.table) <- count.table$Geneid
interval.table <- count.table[,1:6]
count.table <- count.table[,7:ncol(count.table),drop=FALSE]

samples.vec <- sort(colnames(count.table))
groups <- sub("_[^_]+$", "", samples.vec)

DDSFile <- snakemake@output[["dds"]]
if (file.exists(DDSFile) == FALSE) {
    counts <- count.table[,samples.vec,drop=FALSE]
    coldata <- data.frame(row.names=colnames(counts), condition=groups)
    threads <- floor(snakemake@threads[[1]] * 0.75)

    dds <- DESeqDataSetFromMatrix(countData = round(counts), colData = coldata, design = ~ condition)
    dds <- DESeq(dds, parallel=TRUE, BPPARAM=MulticoreParam(ifelse(threads>0, threads, 1)))

    if (!snakemake@params[["vst"]]) {
        rld <- rlog(dds)
    } else {
        rld <- vst(dds)
    }
    save(dds, rld, file=DDSFile)
}

# PCA plot
PlotPCAFile <- snakemake@output[["plot_pca"]]
if (file.exists(PlotPCAFile) == FALSE) {
    pdf(file=PlotPCAFile, onefile=TRUE, width=7, height=7)
    pca.data <- DESeq2::plotPCA(rld, intgroup=c("condition"), returnData=TRUE)
    percentVar <- round(100 * attr(pca.data, "percentVar"))
    plot <- ggplot(pca.data, aes(PC1, PC2, color=condition)) +
            geom_point(size=3) +
            xlab(paste0("PC1: ", percentVar[1], "% variance")) +
            ylab(paste0("PC2: ", percentVar[2], "% variance")) +
            theme(panel.grid.major = element_blank(),
                  panel.grid.minor = element_blank(),
                  panel.background = element_blank(),
                  panel.border = element_rect(colour = "black", fill=NA, size=1))
    print(plot)
    dev.off()
}
```

## Notes for R-analysis agent
- **DESeq2**: Ensure that the first six columns of the featureCounts file are interval information, with sample-specific counts following.
- **Input Data**: Verify that the sample names in the featureCounts file end with "_R1" to represent replicate IDs.
- **Normalization**: The pipeline uses either rlog or vst transformation; check the `vst` parameter in the config.
- **Visualization**: PCA and heatmap plots are generated using ggplot2 and pheatmap; ensure these packages are installed.
- **Reference Genome**: Confirm the correct reference genome build and chromosome are specified in the config.
- **Peak Calling**: MACS2 parameters for p-value and q-value thresholds should be set according to the experimental design.
