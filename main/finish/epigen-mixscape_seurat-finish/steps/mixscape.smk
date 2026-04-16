configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "mixscape"


rule all:
  input:
    "results/finish/mixscape.done"


rule run_mixscape:
  output:
    "results/finish/mixscape.done"
  run:
    run_step(STEP_ID, output[0])
