configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "norm_voom"


rule all:
  input:
    "results/finish/norm_voom.done"


rule run_norm_voom:
  output:
    "results/finish/norm_voom.done"
  run:
    run_step(STEP_ID, output[0])
