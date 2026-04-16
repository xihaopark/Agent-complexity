configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "init_isoform_switch"


rule all:
  input:
    "results/finish/init_isoform_switch.done"


rule run_init_isoform_switch:
  output:
    "results/finish/init_isoform_switch.done"
  run:
    run_step(STEP_ID, output[0])
