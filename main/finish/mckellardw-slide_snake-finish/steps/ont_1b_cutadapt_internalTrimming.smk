configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1b_cutadapt_internalTrimming"


rule all:
  input:
    "results/finish/ont_1b_cutadapt_internalTrimming.done"


rule run_ont_1b_cutadapt_internalTrimming:
  output:
    "results/finish/ont_1b_cutadapt_internalTrimming.done"
  run:
    run_step(STEP_ID, output[0])
