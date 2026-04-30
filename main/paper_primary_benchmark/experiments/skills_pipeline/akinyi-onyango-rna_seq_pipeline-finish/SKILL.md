---
name: pipeline-akinyi-onyango-rna_seq_pipeline-finish
source_type: pipeline
workflow_id: akinyi-onyango-rna_seq_pipeline-finish
workflow_dir: main/finish/workflow_candidates/Akinyi-Onyango__rna_seq_pipeline
generated_at: 2026-04-16T16:55:17Z
model: openrouter/openai/gpt-4o
files_used: 3
chars_used: 6408
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
This pipeline is designed for differential gene expression analysis using RNA-seq data. It processes raw FASTQ files through a series of steps to produce lists of differentially expressed genes between two experimental conditions. The pipeline employs several widely-used bioinformatics tools: FastQC for quality control, Cutadapt for adapter trimming, STAR for read alignment, featureCounts for gene quantification, and DESeq2 for statistical analysis of differential expression. The analysis assumes two conditions with three replicates each and filters for genes with a log2 fold change of at least 2 and an adjusted p-value below 0.05.

## Parameters
- `SAMPLES`: List of sample identifiers (e.g., `["sample_0", "sample_1", "sample_2", "sample_3", "sample_4", "sample_5"]`).
- `CUTADAPT_OPTS`: Options for Cutadapt (`-u 10 -m 25 -q 30`), specifying trimming of the first 10 bases, a minimum length of 25, and a quality cutoff of 30.
- `FEATURECOUNTS_OPTS`: Options for featureCounts (`-g gene_name -s 1`), indicating gene name as the attribute and strandedness.

## Commands / Code Snippets
```r
# DESeq2 analysis script (scripts/deseq_analysis.r)
library(DESeq2)

args <- commandArgs(trailingOnly=TRUE)

countdata <- read.table(args[1], header=T, stringsAsFactors=F)
genenames <- countdata$Geneid
countdata <- countdata[, 7:ncol(countdata)]
colnames(countdata) <- c(paste("sample_",0:5,sep=""))
countdata <- as.matrix(countdata)
rownames(countdata) <- genenames

# Remove all ERCC entries
sel <- sapply(rownames(countdata), function(x){ if(substr(x, 1,5)=="ERCC-"){return(FALSE)}else{return(TRUE)} })
countdata <- countdata[sel, ]

coldata <- data.frame("condition"=as.factor(c(rep("condition_A", 3), rep("condition_B", 3))), row.names=colnames(countdata))

dds <- DESeqDataSetFromMatrix(countData = countdata,
                              colData = coldata,
                              design = ~ condition)

dds <- DESeq(dds)
res <- results(dds)
res <- as.data.frame(res)

res <- res[!is.na(res$log2FoldChange) & !is.na(res$padj), ]
res_up <- res[res$log2FoldChange >= 2, ]
res_down <- res[res$log2FoldChange <= -2, ]

write.table(res_up, file = args[2], col.names = TRUE, row.names = TRUE, quote=FALSE)
write.table(res_down, file = args[3], col.names = TRUE, row.names = TRUE, quote=FALSE)
```

## Notes for R-analysis agent
- The DESeq2 analysis is implemented in `scripts/deseq_analysis.r`. It requires a count matrix with gene identifiers and sample columns, excluding ERCC entries.
- Ensure the count matrix (`featureCounts_output.txt`) is formatted correctly with gene identifiers in the first column and sample counts in subsequent columns.
- The DESeq2 analysis assumes two conditions with three replicates each. Verify that the `colData` matches this structure.
- The pipeline filters for genes with a log2 fold change ≥ 2 or ≤ -2 and an adjusted p-value < 0.05. Double-check these thresholds if different criteria are needed.
- The reference genome and annotation files must be correctly specified in the `generate_index` rule for STAR alignment.
