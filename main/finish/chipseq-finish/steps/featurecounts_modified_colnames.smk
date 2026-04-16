configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "featurecounts_modified_colnames"


rule all:
  input:
    "results/finish/featurecounts_modified_colnames.done"


rule run_featurecounts_modified_colnames:
  output:
    "results/finish/featurecounts_modified_colnames.done"
  run:
    run_step(STEP_ID, output[0])
