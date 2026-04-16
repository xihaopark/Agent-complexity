configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "concat_proteome"


rule all:
  input:
    "results/finish/concat_proteome.done"


rule run_concat_proteome:
  output:
    "results/finish/concat_proteome.done"
  run:
    run_step(STEP_ID, output[0])
