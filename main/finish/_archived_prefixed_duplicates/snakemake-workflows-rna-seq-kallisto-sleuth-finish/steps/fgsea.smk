configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fgsea"


rule all:
  input:
    "results/finish/fgsea.done"


rule run_fgsea:
  output:
    "results/finish/fgsea.done"
  run:
    run_step(STEP_ID, output[0])
