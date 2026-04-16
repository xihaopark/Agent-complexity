configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "featurecounts_deseq2"


rule all:
  input:
    "results/finish/featurecounts_deseq2.done"


rule run_featurecounts_deseq2:
  output:
    "results/finish/featurecounts_deseq2.done"
  run:
    run_step(STEP_ID, output[0])
