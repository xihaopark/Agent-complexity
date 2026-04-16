configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cutadapt_se"


rule all:
  input:
    "results/finish/cutadapt_se.done"


rule run_cutadapt_se:
  output:
    "results/finish/cutadapt_se.done"
  run:
    run_step(STEP_ID, output[0])
