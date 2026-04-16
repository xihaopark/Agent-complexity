configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "goleft_indexcov"


rule all:
  input:
    "results/finish/goleft_indexcov.done"


rule run_goleft_indexcov:
  output:
    "results/finish/goleft_indexcov.done"
  run:
    run_step(STEP_ID, output[0])
