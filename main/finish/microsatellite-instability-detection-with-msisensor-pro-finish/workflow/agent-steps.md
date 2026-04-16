# microsatellite-instability-detection-with-msisensor-pro-finish LLM Execution Spec

## Purpose

- Source repository: `snakemake-workflows__microsatellite-instability-detection-with-msisensor-pro`
- Source snakefile: `../workflow_candidates/snakemake-workflows__microsatellite-instability-detection-with-msisensor-pro/workflow/Snakefile`
- This generated finish workflow exposes the source workflow as stepwise checkpoints.
- Each step corresponds to one source rule or checkpoint discovered from the source Snakemake workflow.

## Operating Rules

- Execute steps in listed order.
- Treat the source workflow as the implementation source of truth.
- Do not mutate the source workflow structure during execution.
- Stop on failure and report the exact source rule that could not be reached.

## Step Order

1. `samtools_index`
2. `download_genome`
3. `msisensor_pro_scan`
4. `msisensor_pro_pro_preprocessing_baseline`
5. `create_panel_of_normals_samples_list`
6. `msisensor_pro_baseline`
7. `msisensor_pro_pro_run`
8. `msisensor_pro_msi`
9. `merge_msi_results`
10. `all`
