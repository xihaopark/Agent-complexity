configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "trimmomatic"


rule all:
  input:
    "results/finish/trimmomatic.done"


rule run_trimmomatic:
  output:
    "results/finish/trimmomatic.done"
  run:
    run_step(STEP_ID, output[0])
