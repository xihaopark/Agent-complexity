configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "eval"


rule all:
  input:
    "results/finish/eval.done"


rule run_eval:
  output:
    "results/finish/eval.done"
  run:
    run_step(STEP_ID, output[0])
