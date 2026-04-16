configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "split_sampleSheet"


rule all:
  input:
    "results/finish/split_sampleSheet.done"


rule run_split_sampleSheet:
  output:
    "results/finish/split_sampleSheet.done"
  run:
    run_step(STEP_ID, output[0])
