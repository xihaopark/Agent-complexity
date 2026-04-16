configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_tumor_from_somatic"


rule all:
  input:
    "results/finish/get_tumor_from_somatic.done"


rule run_get_tumor_from_somatic:
  output:
    "results/finish/get_tumor_from_somatic.done"
  run:
    run_step(STEP_ID, output[0])
