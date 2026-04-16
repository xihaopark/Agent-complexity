configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "featuretypeCounts_length"


rule all:
  input:
    "results/finish/featuretypeCounts_length.done"


rule run_featuretypeCounts_length:
  output:
    "results/finish/featuretypeCounts_length.done"
  run:
    run_step(STEP_ID, output[0])
