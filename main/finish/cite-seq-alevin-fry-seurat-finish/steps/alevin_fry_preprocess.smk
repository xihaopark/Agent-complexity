configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "alevin_fry_preprocess"


rule all:
  input:
    "results/finish/alevin_fry_preprocess.done"


rule run_alevin_fry_preprocess:
  output:
    "results/finish/alevin_fry_preprocess.done"
  run:
    run_step(STEP_ID, output[0])
