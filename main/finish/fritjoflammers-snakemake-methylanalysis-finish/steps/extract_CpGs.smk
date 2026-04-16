configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extract_CpGs"


rule all:
  input:
    "results/finish/extract_CpGs.done"


rule run_extract_CpGs:
  output:
    "results/finish/extract_CpGs.done"
  run:
    run_step(STEP_ID, output[0])
