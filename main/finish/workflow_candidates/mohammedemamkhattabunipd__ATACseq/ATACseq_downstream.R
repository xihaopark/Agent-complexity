# Load the necessary libraries
library(Seurat)
library(tidyverse)
library(Signac)
library(Matrix)

setwd("Downloads/ATACseq/")

# Load the dataset
pbmc2 <- readRDS("pbmc_atac.rds")

DimPlot(pbmc2, reduction = "umap")+
  NoLegend() +
  ggtitle("ATAC-seq data")



#Create gene activity matrix to refelct chromosome regions with genes
#Takes time to finish for me on M1 2020 took about 4 hours
gene_activity_matrix <- GeneActivity(pbmc2) 


# Upload the already created gene activity matrix
gene_activity_matrix <- read.csv("gene_activity_matrix.csv", row.names = 1)
# Remove ".1" suffix from the gene_activity_matrix cell names
colnames(gene_activity_matrix)

gene_activity_matrix <- Matrix(as.matrix(gene_activity_matrix), sparse = TRUE)
colnames(gene_activity_matrix) <- sub("\\.1$", "-1", colnames(gene_activity_matrix))

gene_activity_matrix[1:10,1:10]

# Save the gene activity matrix to a CSV file on your local machine
write.csv(as.matrix(gene_activity_matrix), "gene_activity_matrix.csv")

# Check the class to confirm it's a dgCMatrix
class(gene_activity_matrix)

#Add the gene activity matrix to the Seurat object
pbmc2[["RNA"]] <- CreateAssayObject(counts = gene_activity_matrix)

pbmc2@assays

NormalizeData(pbmc2, assay = "RNA",
              normalization.method = "LogNormalize",
              scale.factor = median(pbmc2$nCount_ATAC))

#interpret the ATAC data from RNA-seq data point of view
DefaultAssay(pbmc2) <- "RNA"
FeaturePlot(pbmc2, features = c("IL7R", "CD3D", "MS4A1", "CD14", "LYZ"),
            pt.size = 0.1, ncol = 3, max.cutoff = "q95")

#Integrate the ATAC and RNA data step1
pbmc_rna <- readRDS("data/pbmc_10k_v3.rds") #Can found in the original vingette site
pbmc_rna <- UpdateSeuratObject(pbmc_rna)
pbmc_rna
View(pbmc_rna@meta.data)

#plot them before integration
a1 <-  DimPlot(pbmc2, reduction = "umap", group.by = "seurat_clusters", label = TRUE) + NoLegend() +
  ggtitle("ATAC-seq data")

r1 <-  DimPlot(pbmc_rna, reduction = "umap", group.by = "celltype", label = TRUE) + NoLegend() +
  ggtitle("RNA-seq data")
a1 | r1

# Integrate the ATAC and RNA data 
transfer.anchors <- FindTransferAnchors(reference = pbmc_rna,
                                        query = pbmc2,
                                        reduction = "pcaproject") #CCA is slow
# Use the anchors to transfer cell type labels
predicted.labels <- TransferData(anchorset = transfer.anchors,
                                 refdata = pbmc_rna$celltype,
                                 weight.reduction = pbmc2[["lsi"]],
                                 dims = 2:30)

predicted.labels

# Add the predicted labels to the query object
pbmc2 <- AddMetaData(pbmc2, metadata = predicted.labels)
head(pbmc2@meta.data)

#plot them after integration
a2 <-  DimPlot(pbmc2, reduction = "umap", group.by = "predicted.id", label = TRUE) + NoLegend() +
  ggtitle("ATAC-seq data")

r2 <-  DimPlot(pbmc_rna, reduction = "umap", group.by = "celltype", label = TRUE) + NoLegend() +
  ggtitle("RNA-seq data")
a2 | r2

# Set the identity of the ATAC-seq object to the predicted labels
Idents(pbmc2) #the clusters
Idents(pbmc2) <- pbmc2$predicted.id #set the identity to the predicted labels

# Find differentially accessible peaks between clusters
DefaultAssay(pbmc2) <- "ATAC"

da <- FindMarkers(pbmc2, ident.1 = "CD4 Naive", ident.2 = "CD14+ Monocytes",
            min.pct = 0.25, test.use = "LR", latent.vars = "nCount_ATAC")

# View the top differentially accessible peaks
head(da)
# Visualize the differentially accessible peaks
da_plot1 <- VlnPlot(pbmc2, features = rownames(da)[1], pt.size = 0.1,
                    idents = c("CD4 Naive", "CD14+ Monocytes"))
da_plot2 <- FeaturePlot(pbmc2, features = rownames(da)[1], pt.size = 0.1) +
  ggtitle(rownames(da)[1])

da_plot1 | da_plot2


#Fold change between two groups of cells
fc <- FoldChange(pbmc2, ident.1 = "CD4 Naive", ident.2 = "CD14+ Monocytes")
fc <- fc[order(fc$avg_log2FC, decreasing = TRUE), ]
View(fc)

#plotting genomic regions ---------
#set plotting order

levels(pbmc2) <- unique(pbmc2$predicted.id)

# Plot the genomic regions for a specific peak
CoveragePlot(object = pbmc2, 
             region = row.names(pbmc2)[1], 
             extend.upstream = 10000, 
             extend.downstream = 10000, 
             group.by = "predicted.id")


CoverageBrowser(pbmc2, region = "CD8A")








