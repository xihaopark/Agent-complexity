configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "clustering"


rule all:
  input:
    "results/finish/clustering.done"


rule run_clustering:
  output:
    "results/finish/clustering.done"
  run:
    run_step(STEP_ID, output[0])
