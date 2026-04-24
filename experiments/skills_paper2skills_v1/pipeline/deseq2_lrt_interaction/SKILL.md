# Pipeline Skill: DESeq2 LRT for Interaction Testing

> Extracted from: snakemake-workflows/rna-seq-star-deseq2 (generalized)
> Generated: Adapted for LRT workflow

## Code Template

```r
library(DESeq2)

# Read input
counts <- read.table("input/counts.tsv", header=TRUE, row.names="gene_id")
coldata <- read.table("input/coldata.tsv", header=TRUE, row.names="sample")

# Create DESeqDataSet with interaction design
dds <- DESeqDataSetFromMatrix(
  countData = counts,
  colData = coldata,
  design = ~ genotype + treatment + genotype:treatment  # interaction model
)

# Filter and run
dds <- dds[rowSums(counts(dds)) >= 10, ]
dds <- DESeq(dds)

# Standard Wald test results
res <- results(dds, name="genotypetreatment.treated")

# Write standard results
write.csv(as.data.frame(res), "output/wald_de.csv")

# Note: For interaction testing, you may need LRT instead of Wald
```

## Common Patterns

- Full model: `~ genotype + treatment + genotype:treatment`
- Reduced model (for LRT): `~ genotype + treatment`
- Interaction coefficient: `genotypeB.treatmentY`

## Notes

This template provides Wald test results. For interaction testing specifically,
consider using `nbinomLRT()` with reduced model for formal interaction testing.
