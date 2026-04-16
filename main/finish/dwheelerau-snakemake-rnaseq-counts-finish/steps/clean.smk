configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "clean"


rule all:
  input:
    "results/finish/clean.done"


rule run_clean:
  output:
    "results/finish/clean.done"
  run:
    run_step(STEP_ID, output[0])
