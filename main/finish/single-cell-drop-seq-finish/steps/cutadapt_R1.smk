configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cutadapt_R1"


rule all:
  input:
    "results/finish/cutadapt_R1.done"


rule run_cutadapt_R1:
  output:
    "results/finish/cutadapt_R1.done"
  run:
    run_step(STEP_ID, output[0])
