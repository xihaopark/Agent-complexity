configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "aggregate_all_clustering_results"


rule all:
  input:
    "results/finish/aggregate_all_clustering_results.done"


rule run_aggregate_all_clustering_results:
  output:
    "results/finish/aggregate_all_clustering_results.done"
  run:
    run_step(STEP_ID, output[0])
