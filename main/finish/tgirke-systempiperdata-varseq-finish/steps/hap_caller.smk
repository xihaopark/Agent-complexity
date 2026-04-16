configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "hap_caller"


rule all:
  input:
    "results/finish/hap_caller.done"


rule run_hap_caller:
  output:
    "results/finish/hap_caller.done"
  run:
    run_step(STEP_ID, output[0])
