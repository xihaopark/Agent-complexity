configfile: "config.yaml"

import glob
import os
import re


# Load config values
MAPQ = config["mapq"]
GENOME = config["genome"]
KEEP_INTERMEDIATE = config.get("keep_intermediate", False)
SKIP_TRIMMING = config.get("skip_trimming", False)

# Function to decide whether to keep intermediate files
def maybe_temp(path):
    return path if KEEP_INTERMEDIATE else temp(path)

# Automatically find all R1 FASTQ files
R1_FILES = []
for ext in ["fastq", "fq", "fastq.gz", "fq.gz"]:
    R1_FILES.extend(glob.glob(f"*.R1.{ext}"))

SAMPLES = []
FASTQ_MAP = {}
for f in R1_FILES:
    sample = re.sub(r"\.R1\.(fastq|fq)(\.gz)?$", "", os.path.basename(f))
    SAMPLES.append(sample)
    r2_candidate = re.sub(r"\.R1\.", ".R2.", f)
    FASTQ_MAP[sample] = {"r1": f, "r2": r2_candidate}

rule all:
    input:
        "multiqc_report.html",
        expand("{sample}_filtered_sorted.bam", sample=SAMPLES),
        expand("{sample}_filtered_sorted.bam.bai", sample=SAMPLES),
        expand("{sample}.bw", sample=SAMPLES)


rule fastqc_raw:
    input:
        r1 = lambda wildcards: FASTQ_MAP[wildcards.sample]["r1"],
        r2 = lambda wildcards: FASTQ_MAP[wildcards.sample]["r2"]

    output:
        r1_html = "{sample}.R1_fastqc.html",
        r2_html = "{sample}.R2_fastqc.html"
    threads: config["threads"]
    shell:
        """
        fastqc {input.r1} {input.r2} --threads {threads}
        """

if not SKIP_TRIMMING:
    rule trim:
        input:
            r1 = lambda wildcards: FASTQ_MAP[wildcards.sample]["r1"],
            r2 = lambda wildcards: FASTQ_MAP[wildcards.sample]["r2"],
            r1_html = rules.fastqc_raw.output.r1_html,
            r2_html = rules.fastqc_raw.output.r2_html
        output:
            r1_trimmed = maybe_temp("{sample}_R1_trimmed.fq.gz"),
            r2_trimmed = maybe_temp("{sample}_R2_trimmed.fq.gz")
        params:
            adapter="TruSeq3-PE.fa"
        threads: config["threads"]
        shell:
            """
            trimmomatic PE -threads {threads} \
                {input.r1} {input.r2} \
                {output.r1_trimmed} /dev/null \
                {output.r2_trimmed} /dev/null \
                ILLUMINACLIP:{params.adapter}:2:30:10 SLIDINGWINDOW:4:20 MINLEN:25
            """

rule align:
    input:
        r1_trimmed = lambda wildcards: FASTQ_MAP[wildcards.sample]["r1"] if SKIP_TRIMMING else f"{wildcards.sample}_R1_trimmed.fq.gz",
        r2_trimmed = lambda wildcards: FASTQ_MAP[wildcards.sample]["r2"] if SKIP_TRIMMING else f"{wildcards.sample}_R2_trimmed.fq.gz"
    output:
        sam = maybe_temp("{sample}_aligned.sam")
    params:
        index=GENOME["bwa_index"]
    threads: config["threads"]

    shell:
        """
        bwa mem -t {threads} {params.index} {input.r1_trimmed} {input.r2_trimmed} > {output.sam}
        """

rule remove_mito:
    input:
        sam="{sample}_aligned.sam"
    output:
        noM_sam= maybe_temp("{sample}_noM.sam")
    shell:
        """
        samtools view -h {input.sam} | awk '$3 != "chrM" || $1 ~ /^@/' > {output.noM_sam}
        """


rule filter_sort_index:
    input:
        noM_sam="{sample}_noM.sam"
    output:
        bam="{sample}_filtered_sorted.bam",
        bai="{sample}_filtered_sorted.bam.bai"
    threads: config["threads"]
    params:
        mapq=MAPQ
    shell:
        """
        samtools view -bS -q {params.mapq} -@ {threads} {input.noM_sam} \
            | samtools sort -@ {threads} -o {output.bam} && \
        samtools index {output.bam}
        """

rule bam_coverage:
    input:
        bam="{sample}_filtered_sorted.bam"
    output:
        bw="{sample}.bw"
    threads: config["threads"]
    shell:
        """
        bamCoverage -b {input.bam} -o {output.bw} --binSize 10 --normalizeUsing CPM -p {threads}
        """

rule call_peaks:
    input:
        bam="{sample}_filtered_sorted.bam"
    output:
        peaks = "{sample}_peaks.narrowPeak" if config["peaktype"] == "narrow" else "{sample}_peaks.broadPeak"
    params:
        species = "hs" if GENOME["name"] == "hg38" else "mm",
        peak_flag = "--broad --broad-cutoff 0.01" if config["peaktype"] == "broad" else "-q 0.01"
    shell:
        """
        macs2 callpeak --shift -100 --extsize 200 --nomodel -t {input.bam} \
            -f BAMPE -n {wildcards.sample} -g {params.species}  {params.peak_flag}
        """


rule atac_qc:
    input:
        bam="{sample}_filtered_sorted.bam",
        peak="{sample}_peaks.narrowPeak"
    output:
        metric_file="{sample}_ataqv_metrics.json"
    params:
        species = "human" if GENOME["name"] == "hg38" else "mouse"
    threads: config["threads"]

    shell:
        """
        ataqv --threads {threads} --name {wildcards.sample} --metrics-file {output.metric_file} \
        --peak-file {input.peak} {params.species} {input.bam}
        """


rule multiqc:
    input:
        bam=expand("{sample}_filtered_sorted.bam", sample=SAMPLES),
        metrics=expand("{sample}_ataqv_metrics.json", sample=SAMPLES)
    output:
        html="multiqc_report.html"
    shell:
        """
        multiqc . --filename {output.html}
        """


