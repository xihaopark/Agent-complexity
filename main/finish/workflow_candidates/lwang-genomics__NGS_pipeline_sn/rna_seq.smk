configfile: "config.yaml"

import glob
import os
import re


# Load config values
MAPQ = config["mapq"]
GENOME = config["genome"]
PSEUDO = config["pseudo"]
KEEP_INTERMEDIATE = config.get("keep_intermediate", False)
SKIP_TRIMMING = config.get("skip_trimming", False)
READ_TYPE = config.get("read_type", "paired")


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

if not PSEUDO: # traditional mapping with STAR
    rule all:
        input:
            "multiqc_report.html",
            expand("{sample}_filtered_sorted.bam", sample=SAMPLES),
            expand("{sample}_filtered_sorted.bam.bai", sample=SAMPLES),
            expand("{sample}.str1.bw", sample=SAMPLES),
            expand("{sample}.str2.bw", sample=SAMPLES),
            expand("{sample}_counts.txt", sample=SAMPLES),
            directory(expand("{sample}_qualimap", sample=SAMPLES))


    if READ_TYPE == "paired" :
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
                fastqc --threads {threads} {input.r1} {input.r2} 
                """

        if not SKIP_TRIMMING:
            rule trim:
                input:
                    r1 = lambda wc: FASTQ_MAP[wc.sample]["r1"],
                    r2 = lambda wc: FASTQ_MAP[wc.sample]["r2"],
                    r1_html = rules.fastqc_raw.output.r1_html,
                    r2_html = rules.fastqc_raw.output.r2_html
                output:
                    r1_trimmed = maybe_temp("{sample}_R1_trimmed.fq.gz"),
                    r2_trimmed = maybe_temp("{sample}_R2_trimmed.fq.gz")
                params:
                    adapter = "TruSeq3-PE.fa"
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
                r1_trimmed = lambda wc: FASTQ_MAP[wc.sample]["r1"] if SKIP_TRIMMING else f"{wc.sample}_R1_trimmed.fq.gz",
                r2_trimmed = lambda wc: (FASTQ_MAP[wc.sample]["r2"] if SKIP_TRIMMING else f"{wc.sample}_R2_trimmed.fq.gz")
            output:
                bam = maybe_temp("{sample}_Aligned.sortedByCoord.out.bam"),
                r1_wig = maybe_temp("{sample}_Signal.Unique.str1.out.wig"),
                r2_wig = maybe_temp("{sample}_Signal.Unique.str2.out.wig"),
                r1_wig_multi = maybe_temp("{sample}_Signal.UniqueMultiple.str1.out.wig"),
                r2_wig_multi = maybe_temp("{sample}_Signal.UniqueMultiple.str2.out.wig")
            params:
                index=GENOME["star_index"]
            threads: config["threads"]

            shell:
                """
                STAR --runThreadN {threads} --genomeDir {params.index} --readFilesIn {input.r1_trimmed} {input.r2_trimmed} \
                --readFilesCommand gzcat --outFileNamePrefix {wildcards.sample}_ --outSAMtype BAM SortedByCoordinate  \
                --outWigType wiggle --outWigStrand Stranded --outWigNorm RPM 
                """

    else:
        rule fastqc_raw:
            input:
                r1 = lambda wildcards: FASTQ_MAP[wildcards.sample]["r1"]

            output:
                r1_html = "{sample}.R1_fastqc.html"

            threads: config["threads"]
            shell:
                """
                fastqc --threads {threads} {input.r1}
                """

        if not SKIP_TRIMMING:
            rule trim:
                input:
                    r1 = lambda wc: FASTQ_MAP[wc.sample]["r1"],
                    r1_html = rules.fastqc_raw.output.r1_html
                output:
                    r1_trimmed = maybe_temp("{sample}_R1_trimmed.fq.gz")
                params:
                    adapter = "TruSeq3-SE.fa"
                threads: config["threads"]
                shell:
                    """
                    trimmomatic SE -threads {threads} \
                        {input.r1} {output.r1_trimmed} \
                        ILLUMINACLIP:{params.adapter}:2:30:10 SLIDINGWINDOW:4:20 MINLEN:25
                    """

        rule align:
            input:
                r1_trimmed = lambda wc: FASTQ_MAP[wc.sample]["r1"] if SKIP_TRIMMING else f"{wc.sample}_R1_trimmed.fq.gz"
            output:
                bam = maybe_temp("{sample}_Aligned.sortedByCoord.out.bam"),
                r1_wig = maybe_temp("{sample}_Signal.Unique.str1.out.wig"),
                r2_wig = maybe_temp("{sample}_Signal.Unique.str2.out.wig"),                
                r1_wig_multi = maybe_temp("{sample}_Signal.UniqueMultiple.str1.out.wig"),
                r2_wig_multi = maybe_temp("{sample}_Signal.UniqueMultiple.str2.out.wig")
            params:
                index=GENOME["star_index"]
            threads: config["threads"]

            shell:
                """
                STAR --runThreadN {threads} --genomeDir {params.index} --readFilesIn {input.r1_trimmed} \
                --readFilesCommand gzcat --outFileNamePrefix {wildcards.sample}_ --outSAMtype BAM SortedByCoordinate  \
                --outWigType wiggle --outWigStrand Stranded --outWigNorm RPM
                """

    rule filter_sort_index:
        input:
            bam = "{sample}_Aligned.sortedByCoord.out.bam"
        output:
            bam="{sample}_filtered_sorted.bam",
            bai="{sample}_filtered_sorted.bam.bai"
        threads: config["threads"]
        params:
            mapq=MAPQ
        shell:
            """
            samtools view -b -q {params.mapq} -@ {threads} {input.bam} \
                | samtools sort -@ {threads} -o {output.bam} && \
            samtools index {output.bam}
            """

    rule convert_bw:
        input:
            wig_str1 = "{sample}_Signal.Unique.str1.out.wig",
            wig_str2 = "{sample}_Signal.Unique.str2.out.wig"
        output:
            bw_str1 = "{sample}.str1.bw",
            bw_str2 = "{sample}.str2.bw"
        params:
            chrom_sizes = GENOME["chrom_sizes"]
        threads: config["threads"]
        shell:
            """
            wigToBigWig {input.wig_str1} {params.chrom_sizes} {output.bw_str1}
            wigToBigWig {input.wig_str2} {params.chrom_sizes} {output.bw_str2}
            """


    rule count_gene:
        input:
            bam = "{sample}_filtered_sorted.bam"
        output:
            counts = "{sample}_counts.txt"
        params:
            paired_flag = "-p" if READ_TYPE == "paired" else "",
            strand_flag = {"none": "-s 0", "forward": "-s 1", "reverse": "-s 2"}[config["strandness"]],
            gtf = GENOME["gtf"]  
        threads: config["threads"]

        shell:
            """
            featureCounts {params.paired_flag} -T {threads} {params.strand_flag} -a {params.gtf} -o {output.counts} {input.bam}
            """

    rule qualimap_qc:
        input:
            bam = "{sample}_filtered_sorted.bam"
        output:
            directory("{sample}_qualimap")
        params:
            strand_flag = {
                "reverse": "strand-specific-reverse",
                "forward": "strand-specific-forward",
                "none": "non-strand-specific"
            }[config["strandness"]],
            gtf = GENOME["gtf"]  
        threads: config["threads"]

        shell:
            """
            qualimap rnaseq -outdir {wildcards.sample}_qualimap -bam {input.bam} -gtf {params.gtf} -p {params.strand_flag} --java-mem-size=4G -outformat PDF
            """


    rule multiqc:
        input:
            expand("{sample}_filtered_sorted.bam", sample=SAMPLES),
            expand("{sample}.str1.bw", sample=SAMPLES),
            expand("{sample}.str2.bw", sample=SAMPLES),
            expand("{sample}_counts.txt", sample=SAMPLES),
            directory(expand("{sample}_qualimap", sample=SAMPLES))
        output:
            html="multiqc_report.html"
        shell:
            """
            multiqc . --filename {output.html}
            """

else: # when pseudo alignment with salmon
    rule all:
        input:
            "multiqc_report.html",
            expand("{sample}.R1_fastqc.html", sample=SAMPLES),
            directory(expand("{sample}_salmon_output", sample=SAMPLES))


    if READ_TYPE == "paired" :
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
                fastqc --threads {threads} {input.r1} {input.r2} 
                """

        if not SKIP_TRIMMING:
            rule trim:
                input:
                    r1 = lambda wc: FASTQ_MAP[wc.sample]["r1"],
                    r2 = lambda wc: FASTQ_MAP[wc.sample]["r2"],
                    r1_html = rules.fastqc_raw.output.r1_html,
                    r2_html = rules.fastqc_raw.output.r2_html
                output:
                    r1_trimmed = maybe_temp("{sample}_R1_trimmed.fq.gz"),
                    r2_trimmed = maybe_temp("{sample}_R2_trimmed.fq.gz")
                params:
                    adapter = "TruSeq3-PE.fa"
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
                r1_trimmed = lambda wc: FASTQ_MAP[wc.sample]["r1"] if SKIP_TRIMMING else f"{wc.sample}_R1_trimmed.fq.gz",
                r2_trimmed = lambda wc: (FASTQ_MAP[wc.sample]["r2"] if SKIP_TRIMMING else f"{wc.sample}_R2_trimmed.fq.gz")
            output:
                bam = directory("{sample}_salmon_output")
            params:
                index=GENOME["salmon_index"]
            threads: config["threads"]

            shell:
                """
                salmon quant -i {params.index} -l A -1 {input.r1_trimmed} -2 {input.r2_trimmed} -p {threads} -o {wildcards.sample}_salmon_output
               """

    else:
        rule fastqc_raw:
            input:
                r1 = lambda wildcards: FASTQ_MAP[wildcards.sample]["r1"]

            output:
                r1_html = "{sample}.R1_fastqc.html"

            threads: config["threads"]
            shell:
                """
                fastqc --threads {threads} {input.r1}
                """

        if not SKIP_TRIMMING:
            rule trim:
                input:
                    r1 = lambda wc: FASTQ_MAP[wc.sample]["r1"],
                    r1_html = rules.fastqc_raw.output.r1_html
                output:
                    r1_trimmed = maybe_temp("{sample}_R1_trimmed.fq.gz")
                params:
                    adapter = "TruSeq3-SE.fa"
                threads: config["threads"]
                shell:
                    """
                    trimmomatic SE -threads {threads} \
                        {input.r1} {output.r1_trimmed} \
                        ILLUMINACLIP:{params.adapter}:2:30:10 SLIDINGWINDOW:4:20 MINLEN:25
                    """

        rule align:
            input:
                r1_trimmed = lambda wc: FASTQ_MAP[wc.sample]["r1"] if SKIP_TRIMMING else f"{wc.sample}_R1_trimmed.fq.gz"
            output:
                bam = directory("{sample}_salmon_output")
            params:
                index=GENOME["salmon_index"]
            threads: config["threads"]

            shell:
                """
                salmon quant -i {params.index} -l A -r {input.r1_trimmed}  -p {threads} -o {wildcards.sample}_salmon_output
               """

    rule multiqc:
        input:
            expand("{sample}.R1_fastqc.html", sample=SAMPLES),
            directory(expand("{sample}_salmon_output", sample=SAMPLES))
        output:
            html="multiqc_report.html"
        shell:
            """
            multiqc . --filename {output.html}
            """




