# NGS_pipeline_sn: A Scalable and Reproducible Snakemake Workflow for RNA-seq, ChIP-seq, and ATAC-seq

**NGS_pipeline_sn** is a modular and fully automated Snakemake workflow designed for robust and reproducible analysis of RNA-seq, ChIP-seq, and ATAC-seq data. Supporting both single-end and paired-end reads, the pipeline integrates standard NGS processing steps—including trimming, alignment, filtering, quantification, peak calling, and QC—while offering flexibility through a centralized config.yaml. With seamless scalability and transparent rule definitions, **NGS_pipeline_sn** is optimized for both local and high-performance computing environments.

## Installation

1. Clone the repository:

Download the pipeline to your local system:
```bash
git clone https://github.com/lwang-genomics/NGS_pipeline_sn.git
```

2. (Optional but recommended) Download default reference files  

This step provides genome index files for commonly used genomes (hg38, mm10) pre-formatted for this pipeline:
```bash
cd NGS_pipeline_sn
bash get_references.sh
```
*All reference genomes compatible with the workflow (e.g., STAR, Salmon, BWA indices) will be organized in the NGS_pipeline_sn/lib/ folder*

## External Dependencies

Please ensure the following tools are installed and accessible from your system PATH:

```text
## Common:
Snakemake
Trimmomatic
SAMtools
FastQC
MultiQC
wigToBigWig
Deeptools

## RNA-seq:
STAR
Salmon
Subread
Qualimap

## ChIP-seq & ATAC-seq:
BWA
MACS2
Aatqv

```
Install dependencies using mamba, conda, or your preferred environment manager.


## Configuration

Edit the config.yaml file to customize:

```text
threads: 4                       # Threads per rule
mapq: 5                          # Minimum MAPQ for filtering
read_type: paired                # "paired" or "single"
pseudo: false                    # true = Salmon mode, false = STAR 
strandness: reverse              # reverse / forward / none
genome:
  star_index: path/to/star/index
  salmon_index: path/to/salmon/index
  gtf: path/to/annotation.gtf
  chrom_sizes: path/to/chrom.sizes
keep_intermediate: false
skip_trimming: false
```

## I. RNA-Seq Processing Pipeline 

This Snakemake pipeline provides a modular and reproducible workflow for processing bulk RNA-seq data, supporting both traditional alignment-based quantification (STAR) and fast pseudo-alignment (Salmon). It automatically detects FASTQ files and processes them through quality control, optional adapter trimming, alignment, quantification, QC, and visualization. Configuration is centralized via a config.yaml file for flexible, multi-sample analysis.


### Features

- Automatic detection of input FASTQ files (\*.R1.fq.gz, \*.R1.fastq, etc.)
- Supports both paired-end and single-end reads
- Optional read trimming with **Trimmomatic**
- Choice of traditional mapping with **STAR** or pseudo-alignment via **Salmon**
- Strand-specific quantification support
- Quality control via **FastQC** and **Qualimap**
- Generation of normalized BigWig files for visualization
- Integrated summary with **MultiQC**
- Configurable species genome choices
- Customizable via a single config.yaml file


### Usage

1. Place rna_seq.smk, config.yaml, and all sample FASTQ files into your working directory.


2. Edit config.yaml to suit your experiment:


3. Run Snakemake 
```
snakemake -s rna_seq.smk --cores 8
```
Optional: Run in background and log output:

```
snakemake -s rna_seq.smk --cores 8 > snakemake.log 2>&1 &
```


### Output Files
Depending on mode (pseudo: false or true), the pipeline generates:

#### STAR mode:

- {sample}_filtered_sorted.bam(.bai) – Filtered and indexed BAM
- {sample}_counts.txt – Gene-level counts from featureCounts
- {sample}.str1.bw, .str2.bw – Strand-specific bigWig tracks
- {sample}_qualimap/ – Qualimap QC folder
- multiqc_report.html – Summary report

#### Salmon mode:
- {sample}_salmon_output/ – Quantification results
- multiqc_report.html – Summary report

### Example Project Structure

```
project/
├── rna_seq.smk
├── config.yaml
├── sample1.R1.fq.gz
├── sample1.R2.fq.gz
├── sample2.R1.fq.gz
├── sample2.R2.fq.gz
└── ...
```


## II. ChIP-Seq Processing Pipeline 

This Snakemake pipeline streamlines the analysis of ChIP-seq data by automating key processing steps for both single-end and paired-end sequencing. Designed for robustness and flexibility, it handles raw FASTQ files through quality control, optional adapter trimming, genome alignment, peak calling, and signal track generation. With a modular structure and centralized configuration via config.yaml, it is well-suited for reproducible, multi-sample ChIP-seq projects across various experimental designs.

### Features

- Automatic detection of input FASTQ files (\*.R1.fq.gz, \*.R1.fastq, etc.)
- Supports both paired-end and single-end reads
- Optional read trimming with **Trimmomatic**
- Read alignment with **BWA**
- Filtering, sorting, and indexing via **SAMtools**
- Peak calling with **MACS2** (configurable for narrow or broad peaks)
- Generation of normalized BigWig files with **deepTools**
- Integrated summary with **MultiQC**
- Possible to provide a customized species genome
- Configurable via a single config.yaml


### Usage
1. Copy and paste chip_seq.smk and config.yaml into your working folder with all sample FASTQ files


2. Modify the config.yaml file as needed


3. Run Snakemake 
```
snakemake -s chip_seq.smk --cores 8
```
Optional: Log output to a file and run in background:

```
snakemake -s chip_seq.smk --cores 8 > snakemake.log 2>&1 &
```


### Output Files
- sampleX_filtered_sorted.bam(.bai) – Filtered, sorted, and indexed BAM files
- sampleX.bw – BigWig signal track normalized by CPM
- sampleX_peaks.narrowPeak or .broadPeak – Peak calls from MACS2
- multiqc_report.html – Combined QC report


### Example Project Structure

```
project/
├── chip_seq.smk
├── config.yaml
├── sample1.R1.fq.gz
├── sample1.R2.fq.gz
├── sample2.R1.fq.gz
├── sample2.R2.fq.gz
└── ...
```




## III. ATAC-Seq Processing Pipeline 

This Snakemake pipeline provides a lightweight, scalable, and reproducible solution for processing ATAC-seq data. It automatically detects paired-end FASTQ files with flexible naming patterns and processes them through trimming, alignment, mitochondrial read removal, filtering, peak calling, QC, and visualization. Configurable via a single config.yaml file, it is ideal for streamlined, multi-sample ATAC-seq analysis in any computing environment.


### Features

- Automatic detection of input FASTQ files (*.R1.fq.gz, *.R1.fastq, etc.)
- Configurable trimming step (can be toggled on/off)
- Read alignment with **BWA**
- Mitochondrial reads removal, filtering and sorting via **SAMtools**
- Peak calling with **MACS2** (configurable for narrow or broad peaks)
- Generation of normalized BigWig files with **deepTools**
- ATAC-specific QC with **ATAQV**
- Integrated summary with **MultiQC**
- Possible to provide a customized species genome
- Configurable via a single config.yaml

### Usage
1. Copy and paste atac_seq.smk and config.yaml into your working folder with all sample FASTQ files


2. Modify the config.yaml file as needed


3. Run snakemake 
```
snakemake -s atac_seq.smk --cores 8
```
Optional: Log output to a file and run in background:

```
snakemake -s atac_seq.smk --cores 8 > snakemake.log 2>&1 &
```

### Output Files
- sampleX_filtered_sorted.bam(.bai) – filtered, sorted, and indexed BAM files
- sampleX.bw – normalized BigWig files
- sampleX_peaks.narrowPeak or broadPeak – peak calls
- sampleX_ataqv_metrics.json – QC metrics
- multiqc_report.html – summary of QC and analysis


### Example Project Structure

```
project/
├── atac_seq.smk
├── config.yaml
├── sample1.R1.fq.gz
├── sample1.R2.fq.gz
├── sample2.R1.fq.gz
├── sample2.R2.fq.gz
└── ...
```

### License

MIT License


### Acknowledgments

This pipeline integrates many excellent open-source bioinformatics tools. Credit goes to the developers of Snakemake, BWA, SAMtools, MACS2, deepTools, MultiQC and so on.



Please let me know if you have any questions or suggestions about my pipeline tool!



