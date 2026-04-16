configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "hisat2_index"


rule all:
  input:
    "results/finish/hisat2_index.done"


rule run_hisat2_index:
  output:
    "results/finish/hisat2_index.done"
  run:
    run_step(STEP_ID, output[0])
