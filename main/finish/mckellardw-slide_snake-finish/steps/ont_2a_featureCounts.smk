configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2a_featureCounts"


rule all:
  input:
    "results/finish/ont_2a_featureCounts.done"


rule run_ont_2a_featureCounts:
  output:
    "results/finish/ont_2a_featureCounts.done"
  run:
    run_step(STEP_ID, output[0])
