configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "genomecov"


rule all:
  input:
    "results/finish/genomecov.done"


rule run_genomecov:
  output:
    "results/finish/genomecov.done"
  run:
    run_step(STEP_ID, output[0])
