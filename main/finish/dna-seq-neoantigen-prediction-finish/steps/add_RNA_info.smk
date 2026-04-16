configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "add_RNA_info"


rule all:
  input:
    "results/finish/add_RNA_info.done"


rule run_add_RNA_info:
  output:
    "results/finish/add_RNA_info.done"
  run:
    run_step(STEP_ID, output[0])
