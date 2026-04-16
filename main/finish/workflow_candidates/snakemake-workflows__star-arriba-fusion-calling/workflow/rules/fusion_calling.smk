rule arriba:
    input:
        unpack(get_optional_arriba_inputs),
        # STAR bam containing chimeric alignments
        bam="<results>/star_align/{sample}/{sample}.sorted_by_coordinate.bam",
        # path to reference genome
        genome=f"<resources>/{genome_name}.fasta",
        # path to annotation gtf
        annotation=f"<resources>/{genome_name}.gtf",
    output:
        # approved gene fusions
        fusions="<results>/arriba_fusions/{sample}/{sample}.tsv",
        # discarded gene fusions
        discarded="<results>/arriba_fusions/{sample}/{sample}.discarded.tsv",  # optional
    log:
        "<logs>/arriba_fusions/{sample}/{sample}.log",
    params:
        # required when any of blacklist or known_fusions is set to True
        genome_build=lookup(within=config, dpath="ref/build"),
        # strongly recommended, see https://arriba.readthedocs.io/en/latest/input-files/#blacklist
        # automatically turned off, if a custom_blacklist file is specified in config
        default_blacklist=(
            False
            if lookup(
                within=config, dpath="params/arriba/custom_blacklist", default=""
            )
            else True
        ),
        # automatically turned off, if a custom_known_fusions file is specified in config
        default_known_fusions=(
            False
            if lookup(
                within=config, dpath="params/arriba/custom_known_fusions", default=""
            )
            else True
        ),
        extra=lookup(within=config, dpath="params/arriba/extra", default=""),
    threads: 1
    wrapper:
        "v9.0.0/bio/arriba"


rule index_fusion_bams:
    input:
        alignments="<results>/star_align/{sample}/{sample}.sorted_by_coordinate.bam",
    output:
        index="<results>/star_align/{sample}/{sample}.sorted_by_coordinate.bam.bai",
    log:
        "<logs>/star_align/{sample}/{sample}.sorted_by_coordinate.index.log",
    params:
        extra="",  # optional params string
    threads: 4  # This value - 1 will be sent to -@
    wrapper:
        "v8.1.1/bio/samtools/index"


rule draw_fusions:
    input:
        fusions="<results>/arriba_fusions/{sample}/{sample}.tsv",
        annotation=f"<resources>/{genome_name}.gtf",
        alignments="<results>/star_align/{sample}/{sample}.sorted_by_coordinate.bam",
        index="<results>/star_align/{sample}/{sample}.sorted_by_coordinate.bam.bai",
    output:
        plots="<results>/arriba_fusions/{sample}/{sample}.fusion_plots.pdf",
    log:
        "<logs>/arriba_fusions/{sample}/{sample}.fusion_plots.log",
    conda:
        "../envs/arriba.yaml"
    params:
        genome_version=branch(
            condition=lookup(
                within=config,
                dpath="ref/build",
            ),
            cases={
                "GRCh37": "hg19_hs37d5_GRCh37",
                "GRCh38": "hg38_GRCh38",
                "GRCm38": "mm10_GRCm38",
                "GRCm39": "mm39_GRCm39",
            },
        ),
    shell:
        '( ARRIBA_RESOURCES_DIR="${{CONDA_PREFIX}}/var/lib/arriba" ; '
        '  ARRIBA_VERSION=$( arriba -h | grep "Version: " | grep -o -P "\d+\.\d+\.\d+" ) ; '
        "  draw_fusions.R "
        "   --fusions={input.fusions} "
        "   --annotation={input.annotation} "
        "   --output={output.plots} "
        "   --alignments={input.alignments} "
        "   --cytobands=${{ARRIBA_RESOURCES_DIR}}/cytobands_{params.genome_version}_v${{ARRIBA_VERSION}}.tsv "
        "   --proteinDomains=${{ARRIBA_RESOURCES_DIR}}/protein_domains_{params.genome_version}_v${{ARRIBA_VERSION}}.gff3 "
        ") >{log} 2>&1 "
