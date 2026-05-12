---
name: pipeline-epigen-rnaseq_pipeline-finish
source_type: pipeline
workflow_id: epigen-rnaseq_pipeline-finish
workflow_dir: main/finish/workflow_candidates/epigen__rnaseq_pipeline
generated_at: 2026-04-16T16:56:30Z
model: openrouter/openai/gpt-4o
files_used: 16
chars_used: 51282
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method
The pipeline is designed for RNA-seq data processing, quantification, and annotation, starting from unmapped BAM files. It performs several key steps: 

1. **Processing**: The pipeline merges BAM files for each sample, converts them to FASTQ format, and performs adapter trimming and quality filtering using `fastp`. The reads are then aligned to a reference genome using the `STAR` aligner, which also quantifies gene expression by counting reads overlapping annotated genes.

2. **Quantification**: The pipeline uses `STAR` in `--quantMode GeneCounts` mode to generate gene expression counts, considering library strandedness. The counts are aggregated into a gene-by-sample matrix using a custom Python script.

3. **Annotation**: Gene annotations are retrieved using the `biomaRt` R package, including Ensembl gene ID, gene symbol, and gene biotype. Exon-based GC content and length are calculated using `GenomicRanges` and `rtracklayer` R packages. The pipeline also generates a sample annotation file integrating input annotations with QC metrics.

The pipeline assumes the user provides a configuration file and an annotation file specifying sample details, including read type and strandedness.

## Parameters
- `mem`: Default is `32000`. Memory allocation in MB.
- `project_name`: Name of the project/dataset.
- `result_path`: Path to the output folder.
- `annotation`: Path to the annotation file.
- `adapter_fasta`: Path to adapter fasta file for `fastp`.
- `fastp_args`: Arguments for `fastp` (default: `"--adapter_sequence auto --trim_poly_g"`).
- `star_args`: Arguments for `STAR` aligner (default: ENCODE standard options).
- `ref.species`: Ensembl species name (default: `homo_sapiens`).
- `ref.release`: Ensembl release version (default: `100`).
- `ref.build`: Genome build (default: `GRCh38`).

## Commands / Code Snippets
```r
# R script for gene annotation using biomaRt
library(tidyverse)
library(GenomicRanges)
library(rtracklayer)
library(Rsamtools)
library("cli")

counts_path <- file.path(snakemake@input[["counts"]])
gtf_path <- file.path(snakemake@input[["gtf"]])
fasta_path <- file.path(snakemake@input[["fasta"]])

gene_annot_path <- file.path(snakemake@output[["gene_annotation"]])

species <- snakemake@params[["species"]]
version <- snakemake@params[["version"]]

mart <- "useast"
rounds <- 0
while ( class(mart)[[1]] != "Mart" ) {
  mart <- tryCatch(
    {
      if (mart == "www") rounds <- rounds + 1
      biomaRt::useEnsembl(
        biomart = "ENSEMBL_MART_ENSEMBL",
        dataset = str_c(species, "_gene_ensembl"),
        version = version,
        mirror = mart
      )
    },
    error = function(e) {
      if (rounds >= 3) {
        cli_abort(
          str_c(
            "Have tried all 4 available Ensembl biomaRt mirrors ",
            rounds,
            " times. You might have a connection problem, or no mirror is responsive.\n",
            "The last error message was:\n",
            message(e)
          )
        )
      }
      mart <- switch(mart,
                     useast = "asia",
                     asia = "www",
                     www = {
                       Sys.sleep(30)
                       "useast"
                     }
              )
    }
  )
}

counts <- read.table(counts_path, sep=',', header=1)

gene_annot <- biomaRt::getBM(
            attributes = c( "ensembl_gene_id",
                            "version",
                            "source",
                            "external_gene_name",
                            "external_gene_source",
                            "description",
                            "gene_biotype"),
            filters = "ensembl_gene_id",
            values = counts$gene,
            mart = mart,
            )

GTF <- import.gff(gtf_path, format="gtf", feature.type="exon")
grl <- reduce(split(GTF, elementMetadata(GTF)$gene_id))
reducedGTF <- unlist(grl, use.names=T)
elementMetadata(reducedGTF)$gene_id <- rep(names(grl), elementNROWS(grl))

FASTA <- FaFile(fasta_path)
open(FASTA)

elementMetadata(reducedGTF)$nGCs <- letterFrequency(getSeq(FASTA, reducedGTF), "GC")[,1]
elementMetadata(reducedGTF)$widths <- width(reducedGTF)

calc_GC_length <- function(x) {
    nGCs = sum(elementMetadata(x)$nGCs)
    width = sum(elementMetadata(x)$widths)
    c(width, nGCs/width)
}
gc_length <- t(sapply(split(reducedGTF, elementMetadata(reducedGTF)$gene_id), calc_GC_length))
colnames(gc_length) <- c("exon_length", "exon_gc")
gc_length <- as.data.frame(gc_length)

gene_annot <- cbind(gene_annot, gc_length[gene_annot$ensembl_gene_id, ])
write.table(gene_annot, file=gene_annot_path, sep=",", quote=TRUE, row.names=FALSE)
```

## Notes for R-analysis agent
- The pipeline uses `biomaRt` for gene annotation; ensure the Ensembl release and species are correctly specified in the config.
- The `GenomicRanges` and `rtracklayer` packages are used to calculate exon-based GC content and length, which are crucial for downstream bias correction.
- The input annotation file must include `sample_name`, `read_type`, `bam_file`, and `strandedness` columns.
- Verify the `fastp` and `STAR` arguments in the config file to ensure they match the experimental setup.
- The pipeline assumes the use of Ensembl annotations; ensure the correct reference genome build is used.
