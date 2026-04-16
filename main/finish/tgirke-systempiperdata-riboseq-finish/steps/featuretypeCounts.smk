configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "featuretypeCounts"


rule all:
  input:
    "results/finish/featuretypeCounts.done"


rule run_featuretypeCounts:
  output:
    "results/finish/featuretypeCounts.done"
  run:
    run_step(STEP_ID, output[0])
