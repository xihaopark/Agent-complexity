# Pipeline Skill: DESeq2 Shrinkage Estimators

> Extracted from: snakemake-workflows/rna-seq-star-deseq2
> Generated: Generic shrinkage workflow

## Code Template

```r
library(DESeq2)

# Read data
counts <- read.table("input/counts.tsv", header=TRUE, row.names="gene_id")
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names="sample")

# Create and run DESeq2
dds <- DESeqDataSetFromMatrix(countData=counts, colData=coldata, design=~condition)
dds <- dds[rowSums(counts(dds)) >= 10, ]
dds <- DESeq(dds)

# Standard shrinkage with ashr
res <- results(dds, name="condition_treated_vs_control")
res_shrunk <- lfcShrink(dds, coef=2, type="ashr", res=res)

# Write output
write.csv(as.data.frame(res_shrunk), "output/shrunk_de.csv")
```

## Common Parameters

- `type="ashr"`: Default in many pipelines (works well generally)
- `type="apeglm"`: Alternative for small samples
- `type="normal"`: Original DESeq2 shrinkage

## Notes

Standard workflow uses "ashr" shrinkage. Compare different estimators
if your task specifically requires comparing shrinkage methods.
