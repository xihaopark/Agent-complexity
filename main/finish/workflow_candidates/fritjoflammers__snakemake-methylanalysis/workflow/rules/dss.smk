# subset gemma relatedness matrix to samples in the methylation dataset
DSS_RUN_LABEL = "default"

DSS_RUN_DIRECTORY = RESULTS_DIR / "DSS" / "by_comparison" / DSS_RUN_LABEL

rule DSS_dmrs:
    input:
        df=rules.methylkit_unite_per_chr_all.output.tibble,
        **metadata_input
    output:
        tsv_dml=DSS_RUN_DIRECTORY / "dmls.{chr}.tsv"),
        tsv_dmr=DSS_RUN_DIRECTORY / "dmrs.{chr}.tsv"),
        plots=DSS_RUN_DIRECTORY / "dmrs.{chr}.pdf"),
    params:
        group1=["sampleA", "sampleB"],
        group2=[
            "sampleC",
            ],
        groups_by_samples=True
    log:
        logs="logs/methylkit_dss.{chr}.log"
    shadow:
        "copy-minimal"
    conda: 
        "../envs/dss.yaml"
    resources:
        **config["RESOURCES"]["medium_small_job"]
    script:
        "../scripts/methylkit_dmr.R" 


# depending on the metadata it is also possible to specify groups by other variable, such as species
use rule DSS_dmrs as DSS_dmrs_2 with:
    output:
        tsv_dml=DSS_RUN_DIRECTORY / "dmls.{chr}.tsv"),
        tsv_dmr=DSS_RUN_DIRECTORY / "dmrs.{chr}.tsv"),
        plots=DSS_RUN_DIRECTORY / "dmrs.{chr}.pdf"),
    params:
        group1=["species_A"],
        group2=["species_B"]

