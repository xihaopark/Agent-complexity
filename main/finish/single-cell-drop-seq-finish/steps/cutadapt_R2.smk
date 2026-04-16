configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cutadapt_R2"


rule all:
  input:
    "results/finish/cutadapt_R2.done"


rule run_cutadapt_R2:
  output:
    "results/finish/cutadapt_R2.done"
  run:
    run_step(STEP_ID, output[0])
