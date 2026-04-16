DESTRAND_CALL_DIR = (
    RESULTS_DIR / "destrand_calls/methylation_calls/methylation_coverage_destranded/"
)


rule extract_CpGs:
    input:
        cov=lambda wildcards: get_input_reads(wildcards, "filename"),
        fasta=config["INPUT"]["FASTA"],
    output:
        bed=DESTRAND_CALL_DIR / "{sample}.cpg.gz",
    conda:
        "../envs/bioscripts.yaml"
    resources:
        runtime=120,
        mem_mb_per_cpu=lambda wildcards, threads, attempt: get_mem_mb_by_attempt(
            wildcards, threads, attempt, 4000
        ),
        tasks=1,
        cpus_per_task=1,
    params:
        chunk_size=10000,
        extra="-m " if TOOL_LABEL == "methyldackel" else " ",
    log:
        RESULTS_DIR / "logs/get_CpG_from_genome/{sample}.log",
    shell:
        "curl https://raw.githubusercontent.com/mobilegenome/bioscripts/main/bioscripts/get_CpG_from_genome/get_CpG_from_genome.py > get_CpG_from_genome.py && "
        "python get_CpG_from_genome.py "
        "-b {input.cov} "
        "-f {input.fasta} "
        "-o {output.bed} "
        "{params.extra} "
        "-c {params.chunk_size} > {log} "


rule destrand_calls:
    input:
        bed_file=rules.extract_CpGs.output.bed,
    output:
        cov=DESTRAND_CALL_DIR / "{sample}.bismark.cov.gz",
    conda:
        "../envs/bioscripts.yaml"
    log:
        RESULTS_DIR / "logs/merge_reverse_strand_calls/{sample}.log",
    resources:
        runtime=120,
        mem_mb_per_cpu=lambda wildcards, threads, attempt: get_mem_mb_by_attempt(
            wildcards, threads, attempt, 8000
        ),
        tasks=1,
        cpus_per_task=1,
    shell:
        "curl https://raw.githubusercontent.com/mobilegenome/bioscripts/main/bioscripts/merge_reverse_strand_calls/merge_reverse_strand_calls.py > merge_reverse_strand_calls.py  && "
        "python merge_reverse_strand_calls.py "
        "-b {input.bed_file} "
        "-o {output.cov} > {log}"
