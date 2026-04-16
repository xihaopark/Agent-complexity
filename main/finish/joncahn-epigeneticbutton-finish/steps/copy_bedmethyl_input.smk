configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "copy_bedmethyl_input"


rule all:
  input:
    "results/finish/copy_bedmethyl_input.done"


rule run_copy_bedmethyl_input:
  output:
    "results/finish/copy_bedmethyl_input.done"
  run:
    run_step(STEP_ID, output[0])
