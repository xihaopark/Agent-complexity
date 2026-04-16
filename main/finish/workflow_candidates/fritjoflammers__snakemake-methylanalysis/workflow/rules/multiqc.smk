
rule multiqc_dir:
    input:
        expand(
            os.path.join(config["OUTPUT_DIR"], "bams/{sample}/{sample}_PE_report.txt"),
            sample=config["SAMPLES"],
        ),
        # expand( + "bismark/{sample}.{ext}",
        # sample=config["SAMPLES"],
        #ext=["_PE_dedup_report.txt",
        #     "M-bias.txt",
        #     "_splitting_report.txt",
        #     "trimming_report.tt"])
    output:
        os.path.join(config["OUTPUT_DIR"], "multiqc/multiqc.html"),
    params:
        extra="",  # Optional: extra parameters for multiqc.
    envmodules:
        "multiqc/1.9",
    resources:
        runtime=60,
        mem_mb_per_cpu=500,
        tasks=1,
        cpus_per_task=1,
    log:
        "logs/multiqc.log",
    wrapper:
        "v2.2.1/bio/multiqc"
