configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "hisat2_mapping"


rule all:
  input:
    "results/finish/hisat2_mapping.done"


rule run_hisat2_mapping:
  output:
    "results/finish/hisat2_mapping.done"
  run:
    run_step(STEP_ID, output[0])
