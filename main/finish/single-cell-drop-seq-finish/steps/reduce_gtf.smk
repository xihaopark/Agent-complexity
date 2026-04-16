configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "reduce_gtf"


rule all:
  input:
    "results/finish/reduce_gtf.done"


rule run_reduce_gtf:
  output:
    "results/finish/reduce_gtf.done"
  run:
    run_step(STEP_ID, output[0])
