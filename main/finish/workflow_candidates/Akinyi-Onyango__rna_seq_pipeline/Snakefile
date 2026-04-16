# RNA-seq Differential Expression Pipeline

# Parameters & Sample List
SAMPLES = ["sample_0","sample_1","sample_2","sample_3","sample_4","sample_5"]

# Adapter trimming options
CUTADAPT_OPTS = "-u 10 -m 25 -q 30"

# featureCounts options
FEATURECOUNTS_OPTS = "-g gene_name -s 1"

# Rule all: Final outputs

rule all:
    input:
        # DESeq2 results
        "results/deseq2/deseq2_up.txt",
        "results/deseq2/deseq2_down.txt",

        # FastQC reports
        expand("results/fastqc_raw/{sample}_fastqc.html", sample=SAMPLES),
        expand("results/fastqc_trimmed/{sample}_trimmed_fastqc.html", sample=SAMPLES)

# Quality Control of FastQ

rule quality_control:
    input:
        "data/raw/{sample}.fastq.gz"
    output:
        "results/fastqc_raw/{sample}_fastqc.html"
    shell:
        "fastqc -o results/fastqc_raw {input}"

# Adapter trimming/ quality filtering

rule quality_filtering:
    input:
        "data/raw/{sample}.fastq.gz"
    output:
        "data/trimmed/{sample}_trimmed.fastq.gz"
    shell:
        "cutadapt {CUTADAPT_OPTS} -o {output} {input}"

# Quality Control of trimmed files 

rule qc_trimmed_files:
    input:
        "data/trimmed/{sample}_trimmed.fastq.gz"
    output:
        "results/fastqc_trimmed/{sample}_trimmed_fastqc.html"
    shell:
        "fastqc -o results/fastqc_trimmed {input}"

# Generate STAR genome index

rule generate_index:
    input:
        genome="reference/genome.fa",
        annotation="reference/annotation.gtf" 
    output:
        directory("reference/genome_files")
    shell:
        "STAR --runMode genomeGenerate --genomeDir {output} --genomeFastaFiles {input.genome} --sjdbGTFfile {input.annotation} --genomeSAindexNbases 11"

# Map reads to reference genome

rule read_mapping:
    input:
        file="data/trimmed/{sample}_trimmed.fastq.gz", 
        index="reference/genome_files/"
    output:
        "results/aligned/{sample}_Aligned.out.sam"
    shell:
        "STAR --readFilesIn {input.file} --readFilesCommand zcat --genomeDir {input.index} --outFileNamePrefix results/aligned/{wildcards.sample}_"

# Count reads per gene

rule read_counts:
    input:
        sam=expand("results/aligned/{sample}_Aligned.out.sam", sample=SAMPLES),
        gtf="reference/annotation.gtf"
    output:
        "results/counts/featureCounts_output.txt"
    shell:
        "featureCounts {FEATURECOUNTS_OPTS} -a {input.gtf} -o {output} {input.sam}"

# Differential expression analysis using DESeq2

rule differential_expression:
    input:
        rscript="scripts/deseq_analysis.r",
        counts="results/counts/featureCounts_output.txt"
    output:
        up="results/deseq2/deseq2_up.txt",
        down="results/deseq2/deseq2_down.txt"
    shell:
        "Rscript {input.rscript} {input.counts} {output.up} {output.down}"
