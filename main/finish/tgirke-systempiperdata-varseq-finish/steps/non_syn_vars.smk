configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "non_syn_vars"


rule all:
  input:
    "results/finish/non_syn_vars.done"


rule run_non_syn_vars:
  output:
    "results/finish/non_syn_vars.done"
  run:
    run_step(STEP_ID, output[0])
