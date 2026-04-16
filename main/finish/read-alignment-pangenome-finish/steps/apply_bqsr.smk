configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "apply_bqsr"


rule all:
  input:
    "results/finish/apply_bqsr.done"


rule run_apply_bqsr:
  output:
    "results/finish/apply_bqsr.done"
  run:
    run_step(STEP_ID, output[0])
