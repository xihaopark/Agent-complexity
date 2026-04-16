# subset gemma relatedness matrix to samples in the methylation dataset
MACAU_RUN_LABEL = "default"

MACAU_RUN_DIRECTORY = RESULTS_DIR / "macau" / "by_model" / MACAU_RUN_LABEL


rule gemma_subset_samples:
    input:
        matrix_file=config["MACAU"]["RUNS"][MACAU_RUN_LABEL]["RELATEDNESS_MATRIX"],
        samples_file=config["MACAU"]["RUNS"][MACAU_RUN_LABEL][
            "RELATEDNESS_SAMPLES_LIST"
        ],
    output:
        relatedness_matrix=MACAU_RUN_DIRECTORY / "relatedness.txt",
        samples_file_subset=MACAU_RUN_DIRECTORY / "samples.txt",
    log:
        RESULTS_DIR / "logs/macau" / MACAU_RUN_LABEL / "gemma_subset_samples.log",
    params:
        samples_list=config["SAMPLES"],
        excluded_samples=config["METHYLKIT"]["EXCLUDE_SAMPLES"],
    conda:
        "../envs/pyread-r.yaml"
    script:
        "../scripts/macau_subset_rel_matrix.py"


# prepare counts file
# Example:
#   site idv1 idv2 idv3 idv4
# site1 2 4 3 8
# site2 3 0 15 9
rule macau_prep_counts_file:
    input:
        meth_data=METHYLKIT_DIR
        / "excl_SNVs"
        / "by_min_samples"
        / "all"
        / "by-chromosome"
        / "df_united.{chr}.rds",
        samples_file=rules.gemma_subset_samples.output.samples_file_subset,
    output:
        read_counts_file=MACAU_RUN_DIRECTORY / "{chr}.read_counts",
        total_counts_file=MACAU_RUN_DIRECTORY / "{chr}.total_counts",
    log:
        RESULTS_DIR / "logs/macau/macau_prep_counts_file.{chr}.log",
    conda:
        "../envs/pyread-r.yaml"
    resources:
        runtime=480,
        mem_mb_per_cpu=lambda wildcards, attempt, threads: get_mem_mb_by_attempt(
            wildcards, attempt, threads, 8000
        ),
        tasks=1,
        cpus_per_task=1,
    script:
        "../scripts/macau_prepare_counts_file.py"


rule extract_column_from_spreadsheet:
    input:
        config["METADATA"]["SAMPLES"],
    output:
        temp(
            MACAU_RUN_DIRECTORY / "extracted_var",
        ),
    log:
        RESULTS_DIR / "logs/macau/extract_column_from_spreadsheet.log",
    conda:
        "../envs/pyread-r.yaml"
    params:
        delim="\t",
        columns=config["MACAU"]["RUNS"][MACAU_RUN_LABEL]["COVARIATES"] + ["sample"],
    script:
        "../scripts/extract_column_from_spreadsheet.py"


# prepare predictor file
# Example:
# 1.2 -0.3 -1.5
# NA 1.5 0.3
# 2.7 1.1 NA
# -0.2 -0.7 0.8
rule macau_prep_variables_file:
    input:
        samples_file=rules.gemma_subset_samples.output.samples_file_subset,
        metadata_file=config["METADATA"]["SAMPLES"],
    output:
        variables_file=MACAU_RUN_DIRECTORY / "predictors",
        variables_columns_file=MACAU_RUN_DIRECTORY / "predictor_columns",
    log:
        RESULTS_DIR / "logs/macau/macau_prep_variables_file.predictors.log",
    params:
        variables=config["MACAU"]["RUNS"][MACAU_RUN_LABEL]["PREDICTOR_VARS"],
        #rename_samples={
        # "old_name": "new_name"   
        #},
    conda:
        "../envs/pyread-r.yaml"
    script:
        "../scripts/macau_prepare_variables_file.py"


# prepare covariate file
# Example:
# 1 1 -1.5
# 1 2 0.3
if config["MACAU"]["RUNS"][MACAU_RUN_LABEL]["COVARIATES"]:

    rule macau_prep_covariate_file:
        input:
            samples_file=rules.gemma_subset_samples.output.samples_file_subset,
            covariate_age=rules.extract_column_from_spreadsheet.output,
        output:
            variables_file=MACAU_RUN_DIRECTORY / "covariates",
            variables_columns_file=MACAU_RUN_DIRECTORY / "covariate_columns",
        log:
            RESULTS_DIR / "logs/macau/macau_prep_variables_file.covariates.log",
        params:
            #rename_samples={
            # "old_name": "new_name"   
            #},
        conda:
            "../envs/pyread-r.yaml"
        script:
            "../scripts/macau_prepare_covariates_file.py"


# run macau
rule macau_run:
    input:
        mcounts_file=rules.macau_prep_counts_file.output.read_counts_file,
        total_counts_file=rules.macau_prep_counts_file.output.total_counts_file,
        predictor_file=rules.macau_prep_variables_file.output.variables_file,
        covariate_file=(
            rules.macau_prep_covariate_file.output.variables_file
            if config["MACAU"]["RUNS"][MACAU_RUN_LABEL]["COVARIATES"]
            else []
        ),
        relatedness_matrix=rules.gemma_subset_samples.output.relatedness_matrix,
    output:
        output_file=MACAU_RUN_DIRECTORY / "macau.{chr}.assoc.txt",
        log=MACAU_RUN_DIRECTORY / "macau.{chr}.log.txt",
    log:
        RESULTS_DIR / "logs/macau/run_macau.{chr}.log",
    params:
        macau_binary=config["MACAU"]["BINARY"],
        sampling_iterations=config["MACAU"]["RUNS"][MACAU_RUN_LABEL][
            "SAMPLING_ITERATIONS"
        ],
    resources:
        **config["RESOURCES"]["medium_small_job"],
    script:
        "../scripts/macau_run.py"
