configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "alignment"


rule all:
  input:
    "results/finish/alignment.done"


rule run_alignment:
  output:
    "results/finish/alignment.done"
  run:
    run_step(STEP_ID, output[0])
