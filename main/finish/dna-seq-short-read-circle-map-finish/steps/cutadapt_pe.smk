configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cutadapt_pe"


rule all:
  input:
    "results/finish/cutadapt_pe.done"


rule run_cutadapt_pe:
  output:
    "results/finish/cutadapt_pe.done"
  run:
    run_step(STEP_ID, output[0])
