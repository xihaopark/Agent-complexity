

import os

configfile: "config.yaml"

CONTRASTS = [f"{c[0]}_vs_{c[1]}" for c in config["contrasts"]]

rule all:
    input:
        expand("results/deseq2/{contrast}.csv", contrast=CONTRASTS),
        expand("results/volcano/{contrast}_volcano.png", contrast=CONTRASTS),
        expand("results/gsea/{contrast}_gsea.csv", contrast=CONTRASTS),
        expand("results/gsea/{contrast}_gsea.png", contrast=CONTRASTS)

# Run DESeq2 per contrast (filtering is done inside deseq2.R)
rule deseq2:
    input:
        counts=config["raw_counts"]
    output:
        csv="results/deseq2/{contrast}.csv"
    params:
        contrast=lambda wildcards: wildcards.contrast
    conda:
        "envs/r_deseq2.yaml"
    script:
        "scripts/deseq2.R"

        
rule volcano:
    input:
        csv="results/deseq2/{contrast}.csv"
    output:
        "results/volcano/{contrast}_volcano.png"
    conda:
        "envs/r_volcano.yaml"
    shell:
        "Rscript scripts/volcanoplot.R {input.csv} {output}"

        
rule gsea:
    input:
        "results/deseq2/{contrast}.csv"
    output:
        table="results/gsea/{contrast}_gsea.csv",
        plot="results/gsea/{contrast}_gsea.png"
    conda:
        "envs/r_gsea.yaml"
    script:
        "scripts/gsea.R"



