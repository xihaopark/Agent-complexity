# Load required library
BiocManager::install("Rsubread")
library(Rsubread)

# Run featureCounts
fc <- featureCounts(
  files = "results/alignments/SRR390728_sorted.bam",
  annot.ext = "ref/Homo_sapiens.GRCh38.111.gtf",
  isGTFAnnotationFile = TRUE,
  GTF.featureType = "exon",
  GTF.attrType = "gene_id",
  isPairedEnd = TRUE,
  nthreads = 4
)

# View output
head(fc$counts)

# Save to file
write.csv(fc$counts, file = "results/gene_counts_SRR390728.csv")
