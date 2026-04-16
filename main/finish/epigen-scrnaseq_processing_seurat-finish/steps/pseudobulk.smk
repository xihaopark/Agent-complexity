configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "pseudobulk"


rule all:
  input:
    "results/finish/pseudobulk.done"


rule run_pseudobulk:
  output:
    "results/finish/pseudobulk.done"
  run:
    run_step(STEP_ID, output[0])
