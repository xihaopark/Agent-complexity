configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "assign_primers"


rule all:
  input:
    "results/finish/assign_primers.done"


rule run_assign_primers:
  output:
    "results/finish/assign_primers.done"
  run:
    run_step(STEP_ID, output[0])
