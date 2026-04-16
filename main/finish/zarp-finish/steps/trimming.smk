configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "trimming"


rule all:
  input:
    "results/finish/trimming.done"


rule run_trimming:
  output:
    "results/finish/trimming.done"
  run:
    run_step(STEP_ID, output[0])
