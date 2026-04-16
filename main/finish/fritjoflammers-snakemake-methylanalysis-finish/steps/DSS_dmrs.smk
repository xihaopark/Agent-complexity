configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "DSS_dmrs"


rule all:
  input:
    "results/finish/DSS_dmrs.done"


rule run_DSS_dmrs:
  output:
    "results/finish/DSS_dmrs.done"
  run:
    run_step(STEP_ID, output[0])
