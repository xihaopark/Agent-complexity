configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_1b_cutadapt2"


rule all:
  input:
    "results/finish/ilmn_1b_cutadapt2.done"


rule run_ilmn_1b_cutadapt2:
  output:
    "results/finish/ilmn_1b_cutadapt2.done"
  run:
    run_step(STEP_ID, output[0])
