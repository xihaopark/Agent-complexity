# Snakemake Methylomics Workflow

This Snakemake workflow is designed to process DNA methylation data using the MethylKit package. It includes several steps for loading, filtering, normalizing, uniting, converting to a tibble format, and performing clustering and PCA analysis.

**This is a public fork of an internally developed workflow and not yet curated and documented for public use. While I do encourage to use and continue developing it, it may not work out of the box for your data and require further generalisation to be useful.**

## Data 

IMPORTANT: See [data/README.md](data/README.md) for information on the data directory and how to use it. 

## Dependencies

Ensure you have the required conda environment set up using the `methylkit.yaml` file located in the `envs` directory.



### pre-commit hook

This repository uses pre-commit to enforce code style. To install the pre-commit hook, run:

```bash
pip3 install pre-commit
pre-commit install
```

The pre-commit hooks are configured using the `.pre-commit-config.yaml` file in the root directory.

## Results

Results are stored in the `results` directory, followed by a label for the workflow run. For example, the results of a workflow run with the label `test` will be stored in the `results/test` directory.

Inside the workflow results directory, you will find the following subdirectories and files: 

- `destrand_calls/`
  - `methylation_calls/methylation_coverage_destranded/{sample}.cpg.gz",`
  - `methylation_coverage_destranded/{sample}.bismark.cov.gz",`
- `methylkit/`
  - `01_load_data/raw.rds`: Raw MethylKit data in RDS format
  - `01_load_data/plots/{sample}.pdf`: Read coverage plots for each sample
  - `02_filt_norm/filtered_normalized.rds`: Filtered and normalized MethylKit data in RDS format
  - `02_filt_norm/filtered_normalized.tsv`: Filtered and normalized MethylKit data in TSV format
  - `02_filt_norm/filt_plots/{sample}.pdf`: Filtering plots for each sample
  - `02_filt_norm/norm_plots/{sample}.pdf`: Filtering plots for each sample
  - `03_split/db/{sample}.txt.{bgz,bgz.tbi}`: BGZipped and indexed files for each sample
  - `04_unite/by_min_samples/`
    - `all` | `x_of_y` 
      - `by-chromosome/united.{chr}.rds`  MethylKit object for for united data
      - `by-chromosome/united_stats.{chr}.tsv`  statistics for united data
      - `by-chromosome/df_united.{chr}.rds` as tibbnle
      - `by-genome/df_mku.rds`
      - `by-genome/statistics.tsv`
  - `05_excl_SNVs/by_min_samples/`
      - `all` | `x_of_y` 
        - `by-chromosome/united.{chr}.rds`  MethylKit object for for united data
        - `by-chromosome/united_stats.{chr}.tsv`  statistics for united data
        - `by-chromosome/df_united.{chr}.rds` as tibbnle
  - `06_analysis/`
    - `clustering/hierarchical_clustering.pdf`: Hierarchical clustering plot
    - `pca/pca.pdf`: PCA plot
- `reports/data_structure.html`: Data structure report
- `logs/`: Log files for each rule
- `macau/`: MACAU results
  - `by-model/`:
    - `{run_label}`:
      - `samples.txt`
      - `relatedness.txt`
      - `{chr}.read_counts`
      - `{chr}.total_counts`
      - `predictors`
      - `predictor_columns`
      - `covariates`
      - `covariate_columns`
      - `macau.{chr}.assoc.txt`
      - `macau.{chr}.log.txt`
- `DSS/`:
  - `by-comparison/`
    - `{comparison_label}`:
      - `samples.tsv`: group-sample information
      - `dss_dmls.{chr}.tsv`: DMLs
      - `dss_dmrs.{chr}.tsv`: DMRs
      - `plots/dmrs.{chr}.pdf`: DMR plots




## Rules

### Rule: methylkit_load

- **Input**: 
  - `samples.filename`: Sample filenames

- **Output**:
  - `raw.rds`: Raw MethylKit data in RDS format
  - `01_read/{sample}.pdf`: Read coverage plots for each sample

- **Log**: `logs/methylkit_load.log`

- **Parameters**:
  - `samples`: List of sample names
  - `min_cov`: Low coverage threshold
  - `assembly_name`: Assembly name

- **Resources**:
  - Runtime: 240 minutes
  - Memory per CPU: 8000 MB
  - Tasks: 1
  - CPUs per task: 1

- **Script**: `scripts/methylkit_load.R`

### Rule: methylkit_filter_normalize

- **Input**: 
  - Output from `methylkit_load`

- **Output**:
  - `filtered_normalized.rds`: Filtered and normalized MethylKit data in RDS format
  - `filtered_normalized.tsv`: Filtered and normalized MethylKit data in TSV format
  - `02_filt/{sample}.pdf`: Filtering plots for each sample
  - `03_norm/{sample}.pdf`: Normalization plots for each sample

- **Log**: `logs/methylkit_filter.log`

- **Parameters**:
  - `high_cov_threshold_perc`: High coverage threshold as a percentage
  - `low_cov_threshold_abs`: Low coverage threshold

- **Resources**:
  - Runtime: 240 minutes
  - Memory per CPU: 4000 MB
  - Tasks: 1
  - CPUs per task: 1

- **Script**: `scripts/methylkit_filt_norm.R`

### Rule: methylkit_unite

- **Input**: 
  - Output from `methylkit_filter_normalize`

- **Output**:
  - `united.rds`: United MethylKit data in RDS format
  - `united.tsv`: United MethylKit data in TSV format

- **Log**: `logs/methylkit_unite.log`

- **Parameters**:
  - `destrand`: Whether to destrand
  - `min_per_group`: Minimum number per group for uniting

- **Resources**:
  - Runtime: 240 minutes
  - Memory per CPU: 8000 MB
  - Tasks: 1
  - CPUs per task: 1

- **Script**: `scripts/methylkit_unite.R`

### Rule: methylkit_mku2tibble

- **Input**: 
  - Output from `methylkit_unite`

- **Output**:
  - `df_mku.rds`: Data in RDS format
  - `united_stats_per_chr.tsv`: United statistics per chromosome

- **Log**: `logs/methylkit_to_tibble.log`

- **Resources**:
  - Runtime: 240 minutes
  - Memory per CPU: 8000 MB
  - Tasks: 1
  - CPUs per task: 1

- **Script**: `scripts/methylkit2tibble.R`

### Rule: methylkit_clustering

- **Input**: 
  - `df`: Data in RDS format from `methylkit_mku2tibble`
  - `metadata_input`

- **Output**:
  - `hierarchical_clustering.pdf`: Hierarchical clustering plot

- **Log**: `logs/methylkit_clustering.log`

- **Resources**:
  - Runtime: 120 minutes
  - Memory per CPU: 1000 MB
  - Tasks: 1
  - CPUs per task: 1

- **Script**: `scripts/methylkit_clustering.R`

### Rule: methylkit_pca

- **Input**: 
  - `rds`: Data in RDS format from `methylkit_unite`
  - `metadata_input`

- **Output**:
  - `pca.pdf`: PCA plot

- **Log**: `logs/methylkit_pca.log`

- **Resources**:
  - Runtime: 120 minutes
  - Memory per CPU: 1000 MB
  - Tasks: 1
  - CPUs per task: 1

- **Script**: `scripts/methylkit_pca.R`

## Execution

To execute this workflow, make sure you have Snakemake installed and create a configuration file with the necessary input paths and parameters. Then, run the workflow using Snakemake with the appropriate target rule.

For example, to run the entire workflow:

```bash
snakemake -s Snakefile
```

To run a specific rule, replace `rule_name` with the desired rule name:

```bash
snakemake -s Snakefile rule_name
```

Please refer to the individual rule descriptions for more details on their inputs and outputs.