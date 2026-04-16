configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bedGraphToBigWig"


rule all:
  input:
    "results/finish/bedGraphToBigWig.done"


rule run_bedGraphToBigWig:
  output:
    "results/finish/bedGraphToBigWig.done"
  run:
    run_step(STEP_ID, output[0])
