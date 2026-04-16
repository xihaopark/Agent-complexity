configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "clean_cutadapt"


rule all:
  input:
    "results/finish/clean_cutadapt.done"


rule run_clean_cutadapt:
  output:
    "results/finish/clean_cutadapt.done"
  run:
    run_step(STEP_ID, output[0])
