configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "concat_somatic"


rule all:
  input:
    "results/finish/concat_somatic.done"


rule run_concat_somatic:
  output:
    "results/finish/concat_somatic.done"
  run:
    run_step(STEP_ID, output[0])
