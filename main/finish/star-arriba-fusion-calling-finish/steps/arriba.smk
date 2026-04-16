configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "arriba"


rule all:
  input:
    "results/finish/arriba.done"


rule run_arriba:
  output:
    "results/finish/arriba.done"
  run:
    run_step(STEP_ID, output[0])
