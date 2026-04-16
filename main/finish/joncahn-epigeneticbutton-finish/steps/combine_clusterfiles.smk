configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "combine_clusterfiles"


rule all:
  input:
    "results/finish/combine_clusterfiles.done"


rule run_combine_clusterfiles:
  output:
    "results/finish/combine_clusterfiles.done"
  run:
    run_step(STEP_ID, output[0])
