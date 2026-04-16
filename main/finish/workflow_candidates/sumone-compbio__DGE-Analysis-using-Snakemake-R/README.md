# Differential Gene Expression (DGE) Analysis with Snakemake and R
Build, customize, and run your own workflow for differential gene expression using Snakemake and R. 

## About the case study: 
### Title: DUX4-r neomorphic activity depending on GTF2I in acute lymphoblastic leukemia [RNA-seq]
##### Description:
The rearranged versions of the transcription factor DUX4 (DUX4-r produced by translocations) are one of the most common causes of B-cell lymphoblastic leukaemia (B-ALL). The study discovered that such rearrangements can lead to both a loss and a gain of function in DUX4-r.

Loss:  Loss of CBP/EP300 transcriptional co-activators interaction and inability to bind and activate repressed chromatin. The rearranged DUX4-r can still bind to DNA but has alterations in its C-terminal transcription activation domain, affecting its interaction with the co-activators CBP and EP300.

Gain: Gain of interaction with the transcription factor GTF2I, redirecting DUX4-r toward leukemogenic targets. Hence, GTF2I can be a potential target to inhibit DUX4-r from causing leukaemia.

## Aim of my study:
How different variants of DUX4, e.g., DUX4 (wild type), DUX4-IGH, and DUX4-del50, impact different genes and associated ontologies, e.g., Biological Pathways.

## Dependencies:
```Anaconda: 25.5.1```, ```Snakemake: 9.10.0```, ```R: 4.4.2```, ```Bioconductor: 3.19```

R and Bioconductor libraries are mentioned in the envs directory for each R script, which will be installed automatically in this pipeline.   

## Methods:
This tutorial walks you through differential gene expression (DGE) analysis using DESeq2 in R, followed by generating a volcano plot to highlight over- and under-expressed genes, and a GSEA plot for pathway enrichment analysis.
The workflow is organized into three R scripts: deseq2.R, volcanoplot.R, and gsea.R.
If you already have your own R scripts for these steps, simply replace mine with yours and follow the instructions below.

Prepare your directory for the Snakemake pipeline as follows:
```
DGE-pipeline/
├── Snakefile
├── config.yaml
├── scripts/
│   ├── deseq2.R
│   ├── volcanoplot.R
│   └── gsea.R
├── data/
│   └── GSE227982_all_counts.xlsx   # gene expression raw counts from this study. 
├── results/
├── envs/
│   ├── r_deseq2.yaml
│   ├── r_volcano.yaml
│   └── r_gsea.yaml
└── README.md
```
In the DGE-pipeline directory, run the following command:
```
snakemake --use-conda --cores 4 --config contrasts='[["IGH","EV"]]'
```
This study involves three experimental conditions—DUX4 (wild type), DUX4-IGH, and DUX4-del50—with EV (Empty Vector) serving as the negative control.

In this example, we are testing the contrast IGH vs EV. You can easily run other contrasts by modifying the contrasts parameter in the Snakemake command—no changes to the R scripts are required.

You can also add more parameters required through ```--config``` in the snakemake command above. To make this work, you should remove hard-coded values from your R scripts and instead let Snakemake pass them as configurable arguments. For example, instead of fixing the FDR cutoff in deseq2.R:
```
fdr_cutoff <- 0.001
```
do this:
```
fdr_cutoff <- snakemake@params[["fdr_cutoff"]]
```
Now you may define the default in the Snakefile:
```
rule deseq2:
    params:
        fdr_cutoff = config.get("fdr_cutoff", 0.001)   # default
    script:
        "scripts/deseq2.R"
```
Now you can dynamically change the cutoff when running Snakemake:
```
snakemake --use-conda --cores 4 \
  --config contrasts='[["IGH","EV"]]' fdr_cutoff=0.05
```

## Results:
### Let's look at the plots of the analysis:

#### 1) PCA Plot
PCA plot of the study. Ideally, each condition should form a distinct cluster as shown here.
![pca_plot_all_condition](https://github.com/sumenties/Differential-Gene-Expression-DGE-Analysis/assets/43076959/ed36cc2f-978f-4fff-81c6-f9f3ef1b8b59)

#### 2) Dispersion Plot
The fitted (red) line should be lower than the dispersion value of 1. 
![dispersion_plot](https://github.com/sumenties/Differential-Gene-Expression-DGE-Analysis/assets/43076959/fdaed0fb-dc4a-4a70-80a0-71ffae5953ad)

#### 3) MA plots for each condition compared to control, i.e., EV in this study. 

##### IGH vs EV
We're interested in outliers here. Outliers at the top are overexpressed genes, and the outliers at the bottom are underexpressed genes. 
![igh_vs_ev](https://github.com/user-attachments/assets/f52b491a-f95f-406c-9b1e-d28f79bca2a7) 

Similarly, MA plots for other conditions can be drawn following the code in the deseq2.R file. 

#### 4) Volcano plot

##### IGH vs EV
Left-hand side: Downregulated genes (log2FoldChange>2, p-adj value < 0.0001)
Right-hand side: Upregulated genes (log2FoldChange<-2, p-adj value < 0.0001)

Significant genes are labelled based on their log2FoldChange and p-adj value.
![igh_vs_ev_vp](https://github.com/sumone-compbio/Differential-Gene-Expression-DGE-Analysis/assets/43076959/5cadb0ff-54fb-4989-a85b-19ae801a20a1)


Significant genes are labelled based on their log2FoldChange and p-adj values. 

#### 5) Dot Plot for GSEA analysis

##### IGH vs EV
![dot_ighvsev](https://github.com/user-attachments/assets/5024555e-67c1-4754-95c7-734d1c3ccdf8)

Here, we're interested in pathways with a high gene ratio (~0.8), i.e., the pathway associated with antigen processing and presentation via class MHC II is being suppressed. Presenting extracellular antigens is necessary for activating CD4+ T cells and thus triggering an immune response. My analysis aligns with immune-evasive activities commonly observed in cancers, where tumour cells alter pathways involved in antigen presentation to escape immune surveillance by hindering the immune system’s ability to detect and present tumour antigens [https://link.springer.com/article/10.1007/s40495-017-0097-y](url).  


##### Link to the study: 
https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227982 
