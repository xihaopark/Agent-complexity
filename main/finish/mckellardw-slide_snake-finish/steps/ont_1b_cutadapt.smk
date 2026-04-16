configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1b_cutadapt"


rule all:
  input:
    "results/finish/ont_1b_cutadapt.done"


rule run_ont_1b_cutadapt:
  output:
    "results/finish/ont_1b_cutadapt.done"
  run:
    run_step(STEP_ID, output[0])
