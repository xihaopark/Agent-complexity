configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "read_counting"


rule all:
  input:
    "results/finish/read_counting.done"


rule run_read_counting:
  output:
    "results/finish/read_counting.done"
  run:
    run_step(STEP_ID, output[0])
