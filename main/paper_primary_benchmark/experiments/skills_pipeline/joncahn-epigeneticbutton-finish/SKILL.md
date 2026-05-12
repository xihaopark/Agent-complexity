---
name: pipeline-joncahn-epigeneticbutton-finish
source_type: pipeline
workflow_id: joncahn-epigeneticbutton-finish
workflow_dir: /Users/park/code/Paper2Skills-main/main/finish/workflow_candidates/joncahn__epigeneticbutton
generated_at: 2026-04-16T19:31:55Z
model: openrouter/openai/gpt-4o
files_used: 11
chars_used: 80000
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
The pipeline is designed to perform comprehensive epigenetic and transcriptomic analyses, integrating multiple data types such as ChIP-seq, ATAC-seq, RNA-seq, mC (methylation), and small RNA-seq. The primary goal is to analyze these data types to understand gene regulation and epigenetic modifications across different conditions and samples. The pipeline includes steps for data preprocessing, quality control, mapping, peak calling, differential expression analysis, and functional enrichment analysis. Key tools and methods used include MACS2 for peak calling, STAR for RNA-seq alignment, and various R packages for downstream analysis such as edgeR for differential expression and topGO for Gene Ontology enrichment.

## Parameters
- `repo_folder`: Path to the repository folder containing the pipeline.
- `analysis_name`: Label for the analysis.
- `full_analysis`: Boolean indicating whether to perform a full analysis.
- `aligned_bams`: Boolean indicating if aligned BAM files are available.
- `trimmed_fastqs`: Boolean indicating if trimmed FASTQ files are available.
- `QC_option`: Options for quality control, e.g., "all".
- `atac_callpeaks.peaktype`: Type of peaks to call in ATAC-seq, e.g., "narrowPeak".
- `atac_tracks.binsize`: Bin size for ATAC-seq coverage tracks.
- `atac_tracks.params`: Additional parameters for ATAC-seq track generation.
- `chip_mapping_option`: Mapping option for ChIP-seq.
- `chip_callpeaks.peaktype`: Type of peaks to call in ChIP-seq.
- `rnaseq_target_file_label`: Label for RNA-seq target file.
- `rnaseq_background_file`: Path to RNA-seq background file.
- `GO`: Boolean indicating whether to perform Gene Ontology analysis.
- `mC_context`: Context for methylation analysis.
- `te_analysis`: Boolean indicating whether to perform transposable element analysis.
- `srna_min_size`: Minimum size for small RNA analysis.
- `srna_max_size`: Maximum size for small RNA analysis.
- `nextflex_v3_deduplication`: Boolean indicating if NextFlex v3 deduplication is used.
- `structural_rna_depletion`: Boolean indicating if structural RNA depletion is performed.

## Commands / Code Snippets
```r
#!/usr/bin/env Rscript

library(edgeR)
library(AnnotationForge)
library(rrvgo)
library(dplyr)
library(topGO)
library(purrr)
library(stringr)

args = commandArgs(trailingOnly=TRUE)

dbname<-args[1]
analysisname<-args[2]
refgenome<-args[3]
targetfile<-args[4]
backgroundfile<-args[5]
targetname<-args[6]

db<-paste0("./genomes/",refgenome,"/GO/")
setwd(db)
if (!requireNamespace(dbname, quietly = TRUE)) {
	install.packages(dbname, repos=NULL, type="source")
}
library(dbname, character.only = TRUE)
info<-read.delim(paste0(dbname,"_",refgenome,"_gaf_file.tab"), header=FALSE)
setwd("../../..")

fGO<-info[,c(1,6,10)]
colnames(fGO)<-c("GID","GO","EVIDENCE")
geneid2GO<-unique(fGO[,c(1,2)])
rn1<-paste(geneid2GO[,1], sep="")
gene2GO<-geneid2GO[,-1]
names(gene2GO)<-rn1

getGO<-function(genelist, target, ont, name) {
	GOdata<-new("topGOdata", 
				ontology = ont, 
				allGenes = genelist,
				annot = annFUN.gene2GO, 
				gene2GO = gene2GO)
	resultFisher<-runTest(GOdata, algorithm = "weight01", statistic = "fisher")
	resultFisherSummary <- summary(attributes(resultFisher)$score <= 0.01)
	nSigTerms<-0
	if (length(resultFisherSummary) == 3) {
		nSigTerms<-as.integer(resultFisherSummary[[3]])
	}
	summary<-GenTable(GOdata, classicFisher = resultFisher, orderBy = "classicFisher", ranksOf = "classicFisher", topNodes = nSigTerms, numChar=1000)
	tab<-summary %>%
		rename_with(.cols = starts_with("apply"), .fn = ~ { if (length(.) > 0) { paste0("classicFisher") } else { . } }) %>%
		mutate(classicFisher = classicFisher %>% str_replace(pattern= "< *1e-30", replacement = "1e-30") %>% as.numeric())
	sigTerms<-tab$GO.ID
	genesInTerms<-genesInTerm(GOdata, sigTerms)
	genesInTerms2<-map(genesInTerms, ~ intersect(.x, myInterestedGenes) %>% paste(collapse = ","))
	tab2<-tab %>% 
		left_join(tibble(GO.ID = names(genesInTerms2), GID = genesInTerms2) %>% 
		tidyr::unnest(GID), by = "GO.ID")
	tab3<-tab %>%
		rename(GO=GO.ID) %>%
		merge(geneid2GO, by="GO") %>%
		merge(target, by="GID") %>%
		arrange(GO) %>%
		unique()
	if (nrow(tab2) > 1) {
		write.table(tab2,paste0("results/RNA/GO/topGO_",name,"_",ont,"_GOs.txt"),sep="\t",row.names=FALSE,col.names=TRUE,quote=FALSE)
	}
	if (nrow(tab3) > 0) {
		write.table(tab3,paste0("results/RNA/GO/topGO_",name,"_",ont,"_GIDs.txt"),sep="\t",row.names=FALSE,col.names=TRUE,quote=FALSE)
	}	
  
	scores<-setNames(-log10(as.numeric(tab$classicFisher)), tab$GO.ID)
	reducedTerms <- tab2 %>%
			rename("go" = "GO.ID", "term" = "Term") %>%
			mutate(parentTerm = term, score = scores)
  
	if (nrow(tab) > 1 ) {
		simMatrix<-calculateSimMatrix(tab$GO.ID,
									orgdb=dbname,
									ont=ont,
									method="Rel")
		if (! is.null(nrow(simMatrix))) {
			reducedTerms<-reduceSimMatrix(simMatrix,
										scores,
										threshold = 0.7,
										orgdb=dbname)
										
			pdf(paste0("results/RNA/plots/topGO_",name,"_",ont,"_treemap.pdf"), width=8, height=8)
			treemapPlot(reducedTerms, size = "score")
			dev.off()
		}
	}
}
```

## Notes for R-analysis agent
- The pipeline uses `edgeR` for differential expression analysis, which requires count data as input.
- Gene Ontology analysis is performed using `topGO`, and the results are visualized with `rrvgo` for reducing redundancy in GO terms.
- Ensure that the reference genome and annotation files are correctly specified in the configuration.
- The pipeline assumes that input files are organized and named according to specific patterns; verify these before running.
- Check the configuration for options related to quality control and analysis steps, such as `QC_option` and `full_analysis`.
- The R scripts rely on specific R packages; ensure they are installed and available in the R environment.
