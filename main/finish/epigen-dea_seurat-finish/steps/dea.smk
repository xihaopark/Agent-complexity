configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "dea"


rule all:
  input:
    "results/finish/dea.done"


rule run_dea:
  output:
    "results/finish/dea.done"
  run:
    run_step(STEP_ID, output[0])
