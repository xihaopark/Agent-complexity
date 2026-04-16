configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "estimate_tmb"


rule all:
  input:
    "results/finish/estimate_tmb.done"


rule run_estimate_tmb:
  output:
    "results/finish/estimate_tmb.done"
  run:
    run_step(STEP_ID, output[0])
