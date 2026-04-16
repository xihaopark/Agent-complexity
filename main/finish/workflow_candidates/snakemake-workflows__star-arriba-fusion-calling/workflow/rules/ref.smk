rule get_genome_fasta:
    output:
        f"<resources>/{genome_name}.fasta",
    log:
        "<logs>/get_genome_fasta.log",
    params:
        species=config["ref"]["species"],
        datatype="dna",
        build=config["ref"]["build"],
        release=config["ref"]["release"],
        chromosome=config["ref"].get("chromosome"),
    cache: "omit-software"
    wrapper:
        "v9.0.0/bio/reference/ensembl-sequence"


rule get_genome_gtf:
    output:
        f"<resources>/{genome_name}.gtf",
    params:
        species=config["ref"]["species"],
        release=config["ref"]["release"],
        build=config["ref"]["build"],
        flavor="",  # optional, e.g. chr_patch_hapl_scaff, see Ensembl FTP.
    log:
        "<logs>/get_genome_gtf.log",
    cache: "omit-software"  # save space and time with between workflow caching (see docs)
    wrapper:
        "v7.4.0/bio/reference/ensembl-annotation"


rule star_index:
    input:
        fasta=f"<resources>/{genome_name}.fasta",
        gtf=f"<resources>/{genome_name}.gtf",
    output:
        directory(f"<resources>/{genome_name}"),
    threads: 8
    params:
        sjdbOverhang=lookup(
            within=config, dpath="params/star/index/sjdbOverhang", default=""
        ),
        extra=lookup(within=config, dpath="params/star/index/extra", default=""),
    log:
        f"<logs>/star_index_{genome_name}.log",
    cache: True
    wrapper:
        "v3.3.7/bio/star/index"
