rule star_align:
    input:
        fq1=get_star_reads_input,
        fq2=lambda wc: get_star_reads_input(wc, True),
        idx=f"<resources>/{genome_name}",
        annotation=f"<resources>/{genome_name}.gtf",
    output:
        aln="<results>/star_align/{sample}/{sample}.sorted_by_coordinate.bam",
        reads_per_gene="<results>/star_align/{sample}/{sample}.reads_per_gene.tsv",
    log:
        "<logs>/star/{sample}.log",
    params:
        # specific parameters to work well with arriba, as documented here:
        # https://github.com/suhrig/arriba/wiki/03-Workflow#demo-script
        # Here, we set the parameters mentioned as an absolute must. In the
        # `config/config.yaml` file we set further recommended paramaters under
        # `params: star: align: extra:`.
        extra=lambda wc, input: (
            "--outSAMtype BAM SortedByCoordinate "
            "--chimOutType WithinBAM SoftClip "
            "--quantMode GeneCounts "
            f"--sjdbGTFfile {input.annotation} "
            f"{get_star_read_group(wc)} "
            f'{lookup(within= config, dpath= "params/star/align/extra", default= "").rstrip()}'
        ),
    threads: 8
    wrapper:
        "v3.3.7/bio/star/align"
