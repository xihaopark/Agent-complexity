configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "datavzrd_methylkit_filt_norm"


rule all:
  input:
    "results/finish/datavzrd_methylkit_filt_norm.done"


rule run_datavzrd_methylkit_filt_norm:
  output:
    "results/finish/datavzrd_methylkit_filt_norm.done"
  run:
    run_step(STEP_ID, output[0])
