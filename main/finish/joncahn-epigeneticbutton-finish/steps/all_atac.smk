configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "all_atac"


rule all:
  input:
    "results/finish/all_atac.done"


rule run_all_atac:
  output:
    "results/finish/all_atac.done"
  run:
    run_step(STEP_ID, output[0])
