configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "norm_cqn"


rule all:
  input:
    "results/finish/norm_cqn.done"


rule run_norm_cqn:
  output:
    "results/finish/norm_cqn.done"
  run:
    run_step(STEP_ID, output[0])
