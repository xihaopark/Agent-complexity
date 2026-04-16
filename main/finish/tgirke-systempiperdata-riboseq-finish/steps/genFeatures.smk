configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "genFeatures"


rule all:
  input:
    "results/finish/genFeatures.done"


rule run_genFeatures:
  output:
    "results/finish/genFeatures.done"
  run:
    run_step(STEP_ID, output[0])
