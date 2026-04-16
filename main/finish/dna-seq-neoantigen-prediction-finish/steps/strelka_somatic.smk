configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "strelka_somatic"


rule all:
  input:
    "results/finish/strelka_somatic.done"


rule run_strelka_somatic:
  output:
    "results/finish/strelka_somatic.done"
  run:
    run_step(STEP_ID, output[0])
