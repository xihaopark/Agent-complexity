configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_cluster_bedfiles"


rule all:
  input:
    "results/finish/make_cluster_bedfiles.done"


rule run_make_cluster_bedfiles:
  output:
    "results/finish/make_cluster_bedfiles.done"
  run:
    run_step(STEP_ID, output[0])
