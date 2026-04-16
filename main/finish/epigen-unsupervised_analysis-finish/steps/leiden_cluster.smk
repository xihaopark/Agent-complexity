configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "leiden_cluster"


rule all:
  input:
    "results/finish/leiden_cluster.done"


rule run_leiden_cluster:
  output:
    "results/finish/leiden_cluster.done"
  run:
    run_step(STEP_ID, output[0])
