configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "methylkit_clustering"


rule all:
  input:
    "results/finish/methylkit_clustering.done"


rule run_methylkit_clustering:
  output:
    "results/finish/methylkit_clustering.done"
  run:
    run_step(STEP_ID, output[0])
