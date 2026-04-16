configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "HLA_LA"


rule all:
  input:
    "results/finish/HLA_LA.done"


rule run_HLA_LA:
  output:
    "results/finish/HLA_LA.done"
  run:
    run_step(STEP_ID, output[0])
