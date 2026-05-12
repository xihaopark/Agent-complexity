library(DESeq2)

args <- commandArgs(trailingOnly=TRUE)

countdata <- read.table(args[1], header=T, stringsAsFactors=F)
genenames <- countdata$Geneid
countdata <- countdata[, 7:ncol(countdata)]
colnames(countdata) <- c(paste("sample_",0:5,sep=""))
countdata <- as.matrix(countdata)
rownames(countdata) <- genenames

#Remove all ERCC entries
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
