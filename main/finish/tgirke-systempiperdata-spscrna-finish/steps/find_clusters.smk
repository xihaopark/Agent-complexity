configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "find_clusters"


rule all:
  input:
    "results/finish/find_clusters.done"


rule run_find_clusters:
  output:
    "results/finish/find_clusters.done"
  run:
    run_step(STEP_ID, output[0])
