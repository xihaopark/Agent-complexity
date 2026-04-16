library(Seurat)
library(tidyverse)
library(Signac)
library(EnsDb.Hsapiens.v86)
library(GenomicRanges)

#Set working directory
setwd("Downloads/ATACseq/")

#frag_file <- read.csv("data/10k_pbmc_ATACv2_nextgem_Chromium_Controller_singlecell.csv", nrows = 10) #, nrows = 10, header = F)
#frag_file

counts <- Read10X_h5("data/10k_pbmc_ATACv2_nextgem_Chromium_Controller_filtered_peak_bc_matrix.h5")
counts[100:110, 100:110]

# Create a Chromatin assay

chrom_assay <- CreateChromatinAssay(
  counts = counts,
  sep = c(":", "-"),
  genome = 'hg19',
  fragments = 'data/10k_pbmc_ATACv2_nextgem_Chromium_Controller_fragments.tsv.gz',
  min.cells = 10,
  min.features = 200
)
str(chrom_assay)

#Check metadata
metadata <- read.csv("data/10k_pbmc_ATACv2_nextgem_Chromium_Controller_singlecell.csv", row.names = 1)
View(metadata)

# Create a Seurat object
# Note: Ensure that the metadata has the same number of rows as the number of cells in the chrom_assay
pbmc <- CreateSeuratObject(
  counts = chrom_assay,
  meta.data = metadata,
  assay = "ATAC",
  min.cells = 10,
  min.features = 200
)  

pbmc@assays$ATAC@annotation


# Add gene annotations from EnsDb
annotations <- GetGRangesFromEnsDb(ensdb = EnsDb.Hsapiens.v86)

annotations
# Ensure that the seqlevels of annotations match the expected format
seqlevelsStyle(annotations) <- "UCSC"

# Add gene annotations to the chromatin assay
pbmc@assays$ATAC@annotation <- annotations

# Check the annotation
pbmc@assays$ATAC@annotation




#Computing QC
pbmc <- NucleosomeSignal(object = pbmc)

#Computing TSS enrichment score
pbmc <- TSSEnrichment(object = pbmc, fast = TRUE)

View(pbmc@meta.data)

#add blacklist ratio and fraction of reads in peaks
pbmc$blacklist_ratio <- pbmc$blacklist_region_fragments / pbmc$peak_region_fragments

pbmc$pct_reads_in_peaks <- pbmc$peak_region_fragments / pbmc$passed_filters * 100

colnames(pbmc@meta.data)

#Visualize QC metrics

a1 <- DensityScatter(object = pbmc, 
                x = "nCount_ATAC", 
                y = "TSS.enrichment", quantiles = TRUE, log_x = TRUE)


a2 <- DensityScatter(object = pbmc, 
               x = "nucleosome_signal", 
               y = "TSS.enrichment", quantiles = TRUE, log_x = TRUE)

a1 | a2


pbmc$nucleosome_group <- ifelse(pbmc$nucleosome_signal > 4, 'NS > 4', 'NS < 4')
h1 <- FragmentHistogram(object = pbmc, group.by = 'nucleosome_group')
h1

v1 <- VlnPlot(object = pbmc, features = c("nCount_ATAC", "nucleosome_signal", "TSS.enrichment", "nFeature_ATAC", "blacklist_ratio"), ncol = 3)
v1
#Filter cells based on QC metrics

# You already calculated TSSEnrichment() — now fix the annotation genome
genome(Annotation(pbmc)) <- "hg19" #because different genome versions can cause issues with TSS enrichment calculation

pbmc <- subset(pbmc, subset = nCount_ATAC > 3000 &
                nCount_ATAC < 30000 &
                TSS.enrichment > 3 & 
                nucleosome_signal < 4 & 
                pct_reads_in_peaks > 15 & 
                blacklist_ratio < 0.05)

# Normalize the data
pbmc <- RunTFIDF(pbmc) #normalizing the counts 
pbmc <- FindTopFeatures(pbmc, min.cutoff = 'q0') # selecting top features 
pbmc <- RunSVD(pbmc) # dimenstionality reduction

v2 <- VlnPlot(object = pbmc, features = c("nCount_ATAC", "nucleosome_signal", "TSS.enrichment", "nFeature_ATAC", "blacklist_ratio"), ncol = 3)
v1 |v2

DepthCor(object = pbmc)
'''Here we see there is a very strong correlation between the first LSI 
component and the total number of counts for the cell. We will perform 
downstream steps without this component as we don’t want to group cells 
together based on their total sequencing depth, but rather by their 
patterns of accessibility at cell-type-specific peaks.'''

#Non linear dimensionality reduction
pbmc <- RunUMAP(pbmc, reduction = "lsi", dims = 2:30) #excluding the first component
pbmc <- FindNeighbors(pbmc, reduction = "lsi", dims = 2:30)
pbmc <- FindClusters(pbmc, algorithm = 4)

# Visualize the clusters
plot_1 <- DimPlot(pbmc, reduction = "umap", label = TRUE, label.size = 5) + NoLegend()
plot_2 <- DimPlot(pbmc, reduction = "lsi", label = TRUE, label.size = 5) + NoLegend()

plot_1

saveRDS(pbmc, file = "pbmc_atac.rds")

  






