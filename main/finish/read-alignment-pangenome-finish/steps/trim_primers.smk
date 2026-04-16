configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "trim_primers"


rule all:
  input:
    "results/finish/trim_primers.done"


rule run_trim_primers:
  output:
    "results/finish/trim_primers.done"
  run:
    run_step(STEP_ID, output[0])
