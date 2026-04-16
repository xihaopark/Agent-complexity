install.packages("BiocManager")
BiocManager::install(c("Rsamtools", "GenomicAlignments", "Gviz"))

library(Rsamtools)
library(GenomicAlignments)
library(Gviz)

bamfile <- "results/alignments/SRR390728_sorted.bam"
reads <- readGAlignments(bamfile)
summary(reads)

# Calculate per-base coverage across the genome
cov <- coverage(reads)

# Compute mean coverage value
mean_cov <- mean(as.numeric(unlist(cov)))
cat("Mean genome-wide coverage:", round(mean_cov, 2), "\n")

library(GenomicRanges)

# Get coverage on chr1
chr1_cov <- cov[["chr1"]]

# Only plot a smaller region for speed (e.g. first 1 million bp)
window_size <- 1e6
chr1_cov_window <- chr1_cov[1:window_size]

# Create one IRanges object per base
coords <- IRanges(start = 1:window_size, width = 1)

# Make GRanges with per-base coverage
gr <- GRanges(seqnames = "chr1",
              ranges = coords,
              score = as.numeric(chr1_cov_window))

# Create the axis and coverage plot
axis <- GenomeAxisTrack()
track <- DataTrack(gr,
                   genome = "hg38",
                   chromosome = "chr1",
                   name = "Coverage",
                   type = "histogram")

# Plot
plotTracks(list(axis, track), from = 1, to = window_size,
           main = "Read Coverage on chr1 (1–1,000,000 bp)")

