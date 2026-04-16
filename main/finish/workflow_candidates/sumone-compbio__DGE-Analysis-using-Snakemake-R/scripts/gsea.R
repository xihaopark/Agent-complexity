#!/usr/bin/env Rscript
suppressPackageStartupMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
  library(enrichplot)
  library(ggplot2)
  library(readr)
  library(dplyr)
  library(stringr)
})

# Snakemake variables
res_file   <- snakemake@input[[1]]
plot_file  <- snakemake@output[["plot"]]
table_file <- snakemake@output[["table"]]

# Load DESeq2 results
res <- read_csv(res_file)
if (!all(c("gene", "log2FoldChange") %in% colnames(res))) {
  stop("The results file must contain 'gene' and 'log2FoldChange' columns")
}

# Prepare ranked gene list exactly like your RStudio version
data.tab_igh <- res
data.tab_igh.order <- data.tab_igh[order(-data.tab_igh$log2FoldChange),]
gene_list_igh <- data.tab_igh.order$log2FoldChange
names(gene_list_igh) <- data.tab_igh.order$gene

cat("Running GSEA with", length(gene_list_igh), "genes...\n")

# Run GSEA exactly like your RStudio version
gse_igh <- gseGO(gene_list_igh, ont = "BP", keyType = "SYMBOL", OrgDb = org.Hs.eg.db, eps = 1e-300, nPermSimple = 10000)

# Check if results exist
if (is.null(gse_igh) || nrow(as.data.frame(gse_igh)) == 0) {
  message("No significant genesets were found for GSEA.")
  write.csv(data.frame(), file = table_file, row.names = FALSE)
  
  png(plot_file, width = 2000, height = 1500, res = 300)
  plot.new()
  text(0.5, 0.5, "No significant genesets found for GSEA", cex = 1.2)
  dev.off()
} else {
  # Save results table
  gse_igh.df <- as.data.frame(gse_igh)
  write.csv(gse_igh.df, file = table_file, row.names = FALSE)
  
  cat("Found", nrow(gse_igh.df), "significant pathways\n")
  
  # Create dotplot exactly like your RStudio version
  plot <- dotplot(gse_igh, showCategory=10, split=".sign") + facet_grid(.~.sign)
  
  # Apply your exact styling
  final_plot <- plot + ggtitle("IGH vs EV") +
    theme(
      axis.text.x = element_text(size = 10, angle = 45, hjust = 1),
      axis.text.y = element_text(size = 10),
      strip.text = element_text(size = 12),
      legend.text = element_text(size = 10),
      legend.title = element_text(size = 12),
      plot.margin = margin(1, 1, 1, 2, "cm"),
      panel.spacing = unit(1, "cm"),
      plot.title = element_text(hjust = 0.5, size = 14)
    ) + 
    scale_y_discrete(expand = expansion(mult = c(0.05, 0.2)))
  
  # Save with larger dimensions to capture full plot
  png(plot_file, width = 4000, height = 2400, res = 300)
  print(final_plot)
  dev.off()
}

cat("GSEA analysis completed successfully\n")
