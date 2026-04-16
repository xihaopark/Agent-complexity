# RNA-seq Differential Expression Pipeline

A reproducible Snakemake workflow for differential gene expression analysis using RNA-seq data, from raw FASTQ files to statistically significant gene lists and visualizations.

---

## Overview

This project implements a full RNA-seq pipeline to identify differentially expressed genes between two experimental conditions. The workflow automates preprocessing, alignment, read counting, and statistical testing, ensuring reproducibility and scalability.  

The analysis follows a standard RNA-seq workflow using widely adopted tools (FastQC, Cutadapt, STAR, featureCounts, and DESeq2) and demonstrates the ability to handle raw NGS data through to biological interpretation.

---

## Workflow

The pipeline consists of the following steps:

1. **Quality Control** – [FastQC](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)  
2. **Adapter Trimming** – [Cutadapt](https://cutadapt.readthedocs.io/en/stable/)  
3. **Read Alignment** – [STAR](https://github.com/alexdobin/STAR)  
4. **Gene Quantification** – [featureCounts](http://subread.sourceforge.net/)  
5. **Differential Expression Analysis** – [DESeq2](https://bioconductor.org/packages/release/bioc/html/DESeq2.html)  

The workflow is implemented using [Snakemake](https://snakemake.readthedocs.io/en/stable/), enabling reproducible and scalable execution.

---

## Data Availability

The original RNA-seq FASTQ files used in this project are not publicly available.  
However, the pipeline is fully reproducible with any RNA-seq dataset.  
To test it, you can download a small public dataset from [SRA](https://www.ncbi.nlm.nih.gov/sra) or use your own FASTQ files.

---

## Files and Directories

The `data/` and `results/` directories are empty in this repo. 
They are placeholders to illustrate the pipeline's structure.
To run the pipeline, add your own FASTQ files and reference genome into `data/`.

## Results

The workflow produces the following key outputs:

- `featureCounts_output.txt` – raw gene count matrix for all samples  
- `deseq2_up.txt` – significantly upregulated genes (log2FC ≥ 2, adjusted p-value < 0.05)  
- `deseq2_down.txt` – significantly downregulated genes (log2FC ≤ -2, adjusted p-value < 0.05)  

---

## Usage

Clone this repository:
```bash
git clone https://github.com/Akinyi-Onyango/rna_seq_pipeline.git
cd rna_seq_pipeline
