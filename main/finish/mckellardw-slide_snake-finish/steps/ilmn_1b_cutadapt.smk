configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_1b_cutadapt"


rule all:
  input:
    "results/finish/ilmn_1b_cutadapt.done"


rule run_ilmn_1b_cutadapt:
  output:
    "results/finish/ilmn_1b_cutadapt.done"
  run:
    run_step(STEP_ID, output[0])
