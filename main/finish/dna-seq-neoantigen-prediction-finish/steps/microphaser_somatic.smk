configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "microphaser_somatic"


rule all:
  input:
    "results/finish/microphaser_somatic.done"


rule run_microphaser_somatic:
  output:
    "results/finish/microphaser_somatic.done"
  run:
    run_step(STEP_ID, output[0])
