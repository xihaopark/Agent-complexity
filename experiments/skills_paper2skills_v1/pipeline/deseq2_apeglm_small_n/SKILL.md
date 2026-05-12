# Pipeline Skill: DESeq2 Differential Expression

> Extracted from: snakemake-workflows/rna-seq-star-deseq2
> Generated: Auto-extracted generic code patterns

## Code Template

```r
library(DESeq2)

# Read input data
counts <- read.table("input/counts.tsv", header=TRUE, row.names="gene_id", sep="\t")
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names="sample", sep="\t")

# Create DESeqDataSet
dds <- DESeqDataSetFromMatrix(
  countData = counts,
  colData = coldata,
  design = ~ condition
)

# Pre-filter low counts
dds <- dds[rowSums(counts(dds)) >= 10, ]

# Run DESeq2
dds <- DESeq(dds)

# Extract results
res <- results(dds, contrast=c("condition", "treated", "control"))

# Shrink LFC (general approach - adjust type as needed)
res <- lfcShrink(dds, coef=2, type="ashr", res=res)

# Write output
write.csv(as.data.frame(res), "output/de_results.csv")
```

## Common Parameters

- `design`: `~ condition` for simple two-group comparison
- `contrast`: `c("condition", "treated", "control")` to specify groups
- `type` for shrinkage: `"ashr"`, `"apeglm"`, or `"normal"`

## Notes

This is a generic DESeq2 workflow pattern. Adapt the specific parameters
(design, contrast, shrinkage type) to your specific task requirements.
