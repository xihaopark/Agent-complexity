#
# data structure
# sample/reference_genome/aligner/methylation_call/
#
# load data into methylkit
# - coverage stats
# - CpG histogram

METHYLKIT_DIR = RESULTS_DIR / "methylkit"

metadata_input = dict(
    sample_metadata=config["METADATA"]["SAMPLES"],
    species_metadata=config["METADATA"]["SPECIES"],
    colors_file=config["SCHEMAS"]["SPECIES_COLORS"],
)


rule methylkit_load:
    input:
        expand(
            DESTRAND_CALL_DIR / "{sample}.bismark.cov.gz",
            sample=config["SAMPLES"],
        ),
    output:
        rds=METHYLKIT_DIR / "load_data" / "raw.rds",  # TODO allow execution for methyldackel and bismark_methylation_extract
        plots=expand(
            METHYLKIT_DIR / "load_data" / "plots" / "{sample}.{ext}",
            sample=config["SAMPLES"],
            ext=["pdf", "svg"],
        ),
        report=report(
            directory(Path(METHYLKIT_DIR / "load_data" / "plots")),
            patterns=["{sample}.pdf"],
            category="methylkit_load",
            subcategory="{sample}",
        ),
        # TODO coverage_stats=
        # TODO cpg_histogram=
        # TODO stats_csv=
    log:
        logs=RESULTS_DIR / "logs/methylkit_load.log",
    conda:
        "../envs/methylkit.yaml"
    params:
        samples=config["SAMPLES"],
        min_cov=config["METHYLKIT"]["LOW_COV_THRESHOLD"],
        assembly_name="individual",
        calling_tool=TOOL_LABEL,
    shadow:
        "copy-minimal"
    resources:
        **config["RESOURCES"]["big_job"],
    script:
        "../scripts/methylkit_load.R"


# filtering
rule methylkit_filter_normalize:
    input:
        rules.methylkit_load.output.rds,
    output:
        rds=METHYLKIT_DIR / "filt_norm" / "filtered_normalized.rds",
        stats_tsv=METHYLKIT_DIR / "filt_norm" / "filtered_normalized.tsv",
        plots_filt=report(
            expand(
                METHYLKIT_DIR / "filt_norm" / "filt_plots" / "{sample}.pdf",
                sample=config["SAMPLES"],
            ),
            patterns=["*.pdf"],
            category="methylkit_filt",
            subcategory="by-sample",
        ),
        plots_norm=report(
            expand(
                METHYLKIT_DIR / "filt_norm" / "norm_plots" / "{sample}.pdf",
                sample=config["SAMPLES"],
            ),
            patterns=["*.pdf"],
            category="methylkit_norm",
            subcategory="by-sample",
        ),
        # coverage_stats=
        # coverage_stats=
    log:
        logs=RESULTS_DIR / "logs/methylkit_filter.log",
    conda:
        "../envs/methylkit.yaml"
    shadow:
        "copy-minimal"
    params:
        high_cov_threshold_perc=config["METHYLKIT"]["HIGH_COV_THRESHOLD_PERC"],
        low_cov_threshold_abs=config["METHYLKIT"]["LOW_COV_THRESHOLD"],
    resources:
        **config["RESOURCES"]["huge_job"],
    script:
        "../scripts/methylkit_filt_norm.R"


rule datavzrd_methylkit_filt_norm:
    input:
        config=workflow.source_path(
            "../resources/datavzrd/methylkit_filt_norm.datavzrd.yaml"
        ),
        table=rules.methylkit_filter_normalize.output.stats_tsv,
    params:
        extra="",
    output:
        report(
            directory(
                RESULTS_DIR / "report/datavzrd-report/methylkit_filt_norm_stats"
            ),
            htmlindex="index.html",
            category="methylkit_norm",
        ),
    log:
        RESULTS_DIR / "logs/datavzrd_report/filt_norm.log",
    wrapper:
        "v3.11.0/utils/datavzrd"


# # split
rule methylkit_split:
    input:
        rules.methylkit_filter_normalize.output.rds,
    output:
        dbfiles=expand(
            METHYLKIT_DIR / "split" / "db/{sample}.txt.bgz",
            sample=config["SAMPLES"],
        ),
        dbindices=expand(
            METHYLKIT_DIR / "split" / "db/{sample}.txt.bgz.tbi",
            sample=config["SAMPLES"],
        ),
    log:
        logs=RESULTS_DIR / "logs/methylkit_split.log",
    shadow:
        "copy-minimal"
    conda:
        "../envs/methylkit.yaml"
    threads: 4
    resources:
        **config["RESOURCES"]["mk_unite_96samples"],
    script:
        "../scripts/methylkit_split.R"


# # unite
rule methylkit_unite_per_chr_all:
    input:
        dbfiles=rules.methylkit_split.output.dbfiles,
        dbindices=rules.methylkit_split.output.dbindices,
    output:
        rds=METHYLKIT_DIR
        / "unite"
        / "by_min_samples"
        / "all"
        / "by-chromosome"
        / "united.{chr}.rds",
        tibble=METHYLKIT_DIR
        / "unite"
        / "by_min_samples"
        / "all"
        / "by-chromosome"
        / "df_united.{chr}.rds",
        stats_tsv=METHYLKIT_DIR
        / "unite"
        / "by_min_samples"
        / "all"
        / "by-chromosome"
        / "united_stats.{chr}.tsv",
    wildcard_constraints:
        chr="|".join(CHROMOSOMES),
    log:
        logs=RESULTS_DIR / "logs/methylkit_unite.all.{chr}.log",
    shadow:
        "copy-minimal"
    conda:
        "../envs/methylkit.yaml"
    threads: 4
    resources:
        **config["RESOURCES"]["medium_job"],
    params:
        destrand=False,
        use_db=True,
        min_per_group=len(config["SAMPLES"]),
        exclude=config["METHYLKIT"]["EXCLUDE_SAMPLES"],
    script:
        "../scripts/methylkit_unite_per_chr.R"


use rule methylkit_unite_per_chr_all as methylkit_unite_per_chr_64 with:
    output:
        rds=METHYLKIT_DIR
        / "unite"
        / "by_min_samples"
        / "64"
        / "by-chromosome"
        / "united.{chr}.rds",
        tibble=METHYLKIT_DIR
        / "unite"
        / "by_min_samples"
        / "64"
        / "by-chromosome"
        / "df_united.{chr}.rds",
        stats_tsv=METHYLKIT_DIR
        / "unite"
        / "by_min_samples"
        / "64"
        / "by-chromosome"
        / "united_stats.{chr}.tsv",
    log:
        logs=RESULTS_DIR / "logs/methylkit_unite.64.{chr}.log",
    params:
        destrand=False,
        use_db=True,
        min_per_group=64,
        exclude=config["METHYLKIT"]["EXCLUDE_SAMPLES"],


# remove C-T SNPs
rule methylkit_remove_variant_sites:
    input:
        tibble=rules.methylkit_unite_per_chr_all.output.tibble,
        exclusion_variants_bedfile=config["INPUT"]["EXCLUSION_VARIANTS_BED"],
    output:
        tibble=METHYLKIT_DIR
        / "excl_SNVs"
        / "by_min_samples"
        / "all"
        / "by-chromosome"
        / "df_united.{chr}.rds",
        stats_tsv=report(
            METHYLKIT_DIR
            / "excl_SNVs"
            / "by_min_samples"
            / "all"
            / "by-chromosome"
            / "united_stats.{chr}.tsv",
            patterns=["*.tsv"],
            category="methylkit_remove_snps",
            subcategory="{chr}",
        ),
        # TODO: also provide methylkit object without SNPs
    log:
        logs=RESULTS_DIR / "logs/methylkit_remove_snps.min_ALL_per_group.{chr}.log",
    shadow:
        "copy-minimal"
    conda:
        "../envs/methylkit.yaml"
    resources:
        **config["RESOURCES"]["medium_job"],
    script:
        "../scripts/methylkit_remove_snvs.R"


# convert to tibble
rule methylkit_split_mku2tibble:
    input:
        rds_list=expand(
            METHYLKIT_DIR
            / "unite"
            / "by_min_samples"
            / "{{min_per_group}}"
            / "by-chromosome"
            / "united.{chr}.rds",
            chr=CHROMOSOMES,
        ),
    output:
        rds=METHYLKIT_DIR
        / "unite"
        / "by_min_samples"
        / "{min_per_group}"
        / "by-genome"
        / "df_mku.rds",
        stats_tsv=METHYLKIT_DIR
        / "unite"
        / "by_min_samples"
        / "{min_per_group}"
        / "by-genome"
        / "statistics.tsv",
    log:
        logs=RESULTS_DIR / "logs/methylkit_to_tibble_{min_per_group}.log",
    shadow:
        "copy-minimal"
    conda:
        "../envs/methylkit.yaml"
    resources:
        **config["RESOURCES"]["bigger_job"],
    script:
        "../scripts/methylkit2tibble_split.R"


rule datavzrd_methylkit_unite:
    input:
        # the config file may be a yte template, with access to input, params and wildcards
        # analogous to Snakemake's generic template support:
        # https://snakemake.readthedocs.io/en/stable/snakefiles/rules.html#template-rendering-integration
        # For template processing, __use_yte__: true has to be stated in the config file
        config=workflow.source_path(
            "../resources/datavzrd/methylkit_unite.datavzrd.yaml"
        ),
        # optional files required for rendering the given config
        table=METHYLKIT_DIR
        / "unite"
        / "by_min_samples"
        / "{min_samples}"
        / "by-genome"
        / "statistics.tsv",
    params:
        extra="",
    output:
        report(
            directory(
                RESULTS_DIR
                / "report/datavzrd-report/methylkit_unite_{min_samples}_genome_stats"
            ),
            htmlindex="index.html",
            category="methylkit_unite_{min_samples}",
        ),
    log:
        RESULTS_DIR / "logs/datavzrd_report/{min_samples}.log",
    wrapper:
        "v3.11.0/utils/datavzrd"


# TODO: add rule to combine all chromosomes into one tibble after removing SNVs


# # clustering
rule methylkit_clustering:
    input:
        **metadata_input,
        df=rules.methylkit_split_mku2tibble.output.rds,
    output:
        clustering_circular=report(
            RESULTS_DIR
            / "analysis"
            / "{min_per_group}"
            / "clustering"
            / "hierarchical_clustering.pdf",
            patterns=["*.pdf"],
            category="analysis",
            subcategory="all",
        ),
    log:
        logs=RESULTS_DIR / "logs/methylkit_clustering.{min_per_group}.log",
    shadow:
        "copy-minimal"
    conda:
        "../envs/methylkit.yaml"
    resources:
        **config["RESOURCES"]["huge_job"],
    script:
        "../scripts/methylkit_clustering.R"


# # clustering
rule methylkit_pca:
    input:
        **metadata_input,
        rds=rules.methylkit_unite_per_chr_all.output.tibble,
    output:
        pca_plot=report(
            RESULTS_DIR / "analysis" / "{min_per_group}" / "pca" / "pca.{chr}.pdf",
            patterns=["*.pdf"],
            category="analysis",
            subcategory="all",
        ),
    log:
        logs=RESULTS_DIR / "logs/methylkit_pca.{min_per_group}.{chr}.log",
    shadow:
        "copy-minimal"
    conda:
        "../envs/methylkit.yaml"
    resources:
        runtime=120,
        mem_mb_per_cpu=12000,
        tasks=1,
        cpus_per_task=1,
    script:
        "../scripts/methylkit_pca.R"


rule notebook_data_structure:
    input:
        **metadata_input,
        rds=expand(
            METHYLKIT_DIR
            / "unite"
            / "by_min_samples"
            / "all"
            / "by-chromosome"
            / "df_united.{chr}.rds",
            chr=CHROMOSOMES,
        ),
        exclusion_variants_bedfile=config["INPUT"]["EXCLUSION_VARIANTS_BED"],
        repeats_rds=config["INPUT"]["REPEATS_RDS"],
        wheatearcommons_repo_dir="data/wheatearcommons",
    output:
        report=RESULTS_DIR
        / "analysis"
        / "{min_per_group}"
        / "reports"
        / "data_structure.html",
        pca_object=RESULTS_DIR
        / "analysis"
        / "{min_per_group}"
        / "pca"
        / "pca_results.rds",
    log:
        RESULTS_DIR / "logs/quarto_data_structure.{min_per_group}.log",
    conda:
        "../envs/methylkit.yaml"
    params:
        output_format="html",
    resources:
        runtime=120,
        mem_mb_per_cpu=256000,
        tasks=1,
        cpus_per_task=1,
    script:
        "../scripts/quarto-data_structure.py"
