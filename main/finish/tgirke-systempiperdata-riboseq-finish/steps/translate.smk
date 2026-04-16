configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "translate"


rule all:
  input:
    "results/finish/translate.done"


rule run_translate:
  output:
    "results/finish/translate.done"
  run:
    run_step(STEP_ID, output[0])
