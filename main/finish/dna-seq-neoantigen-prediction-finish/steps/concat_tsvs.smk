configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "concat_tsvs"


rule all:
  input:
    "results/finish/concat_tsvs.done"


rule run_concat_tsvs:
  output:
    "results/finish/concat_tsvs.done"
  run:
    run_step(STEP_ID, output[0])
