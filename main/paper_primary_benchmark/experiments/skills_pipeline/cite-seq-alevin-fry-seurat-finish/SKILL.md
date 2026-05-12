---
name: pipeline-cite-seq-alevin-fry-seurat-finish
source_type: pipeline
workflow_id: cite-seq-alevin-fry-seurat-finish
workflow_dir: main/finish/workflow_candidates/snakemake-workflows__cite-seq-alevin-fry-seurat
generated_at: 2026-04-16T16:56:38Z
model: openrouter/openai/gpt-4o
files_used: 18
chars_used: 19722
generator: experiments/skills_pipeline/tools/generate_pipeline_skill.py
---

## Method

This pipeline is designed for the analysis of CITE-seq data, integrating RNA and protein expression data from single cells. It uses alevin-fry for the quantification of RNA, ADT (antibody-derived tags), and HTO (hashtag oligonucleotides) from sequencing data. The pipeline then processes these quantifications using Seurat for downstream analysis, including normalization, demultiplexing, and visualization. The workflow begins by obtaining reference genome and annotation data, followed by read mapping using Salmon and alevin-fry. The quantifications are loaded into Seurat objects, where normalization and filtering steps are applied to remove unwanted cells and identify singlets. Visualization steps include plotting count distributions and generating UMAP embeddings to explore cell populations.

## Parameters

- `reference.species`: Default is `homo_sapiens`. Specifies the species for reference genome and annotation.
- `reference.build`: Default is `GRCh38`. Specifies the genome build version.
- `reference.release`: Default is `100`. Specifies the Ensembl release version.
- `samples.rna.sra`: Default is `SRR8758323`. SRA accession for RNA sample.
- `samples.adt.sra`: Default is `SRR8758325`. SRA accession for ADT sample.
- `samples.hto.sra`: Default is `SRR8758327`. SRA accession for HTO sample.
- `samples.rna.geometry`: Specifies read, barcode, and UMI geometry for RNA sample.
- `samples.adt.geometry`: Specifies read, barcode, and UMI geometry for ADT sample.
- `samples.hto.geometry`: Specifies read, barcode, and UMI geometry for HTO sample.
- `antibodies.adt-seqs`: Path to ADT sequences file, default is `data/adt.tsv`.
- `antibodies.hto-seqs`: Path to HTO sequences file, default is `data/hto.tsv`.
- `thresholds.max-hto-count`: Default is `null`. Upper bound for HTO counts to consider.
- `thresholds.max-adt-count`: Default is `null`. Upper bound for ADT counts to consider.

## Commands / Code Snippets

```r
# Load quantifications into Seurat object
hto_q <- load_fry(snakemake@input[["hto"]], verbose = TRUE)
adt_q <- load_fry(snakemake@input[["adt"]], verbose = TRUE)
rna_q <- load_fry(snakemake@input[["rna"]], verbose = TRUE)

common.cells <- intersect(colnames(rna_q), colnames(adt_q))
common.cells <- intersect(common.cells , colnames(hto_q))

gid_to_gname <- read.table(snakemake@input[["geneid2name"]])
rownames(rna_q) <- gid_to_gname$V2[match(rownames(rna_q), gid_to_gname$V1)]

seurat_object <- CreateSeuratObject(counts(rna_q)[, which(colnames(rna_q) %in% common.cells)])
seurat_object[["ADT"]] <- CreateAssayObject(counts = counts(adt_q)[, which(colnames(adt_q) %in% common.cells)])
seurat_object[["HTO"]] <- CreateAssayObject(counts = counts(hto_q)[, which(colnames(hto_q) %in% common.cells)])

saveRDS(seurat_object, snakemake@output[[1]])
```

```r
# Filter and normalize HTO data
object <- subset(object, subset = nCount_HTO < snakemake@params[["max_hto_count"]])
DefaultAssay(object) <- "HTO"
object <- NormalizeData(object, normalization.method = "CLR", margin = 2, verbose = F)
VariableFeatures(object) <- rownames(object[["HTO"]]@counts)
object <- ScaleData(object, assay = "HTO", verbose = F)
object <- HTODemux(object, assay = "HTO", positive.quantile = 0.99, verbose = F)
Idents(object) <- "HTO_classification.global"
saveRDS(object, snakemake@output[[1]])
```

## Notes for R-analysis agent

- The pipeline uses the Seurat package extensively for single-cell analysis, including functions like `CreateSeuratObject`, `NormalizeData`, `HTODemux`, and `RunUMAP`.
- Ensure the input data for RNA, ADT, and HTO quantifications are correctly formatted and contain matching cell barcodes for integration.
- The gene ID to name mapping is crucial for RNA data; verify the `geneid2name.tsv` file is correctly generated and used.
- The pipeline assumes the presence of a `max-hto-count` threshold for filtering; ensure this is set appropriately based on initial plots.
- UMAP embeddings are generated using PCA reduction; check the dimensions and reduction method settings.
- The pipeline is based on the Ensembl GRCh38 build; ensure compatibility with the reference genome and annotation files.
