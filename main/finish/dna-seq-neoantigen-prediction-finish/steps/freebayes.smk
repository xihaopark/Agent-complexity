configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "freebayes"


rule all:
  input:
    "results/finish/freebayes.done"


rule run_freebayes:
  output:
    "results/finish/freebayes.done"
  run:
    run_step(STEP_ID, output[0])
