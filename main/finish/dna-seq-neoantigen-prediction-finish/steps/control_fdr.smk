configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "control_fdr"


rule all:
  input:
    "results/finish/control_fdr.done"


rule run_control_fdr:
  output:
    "results/finish/control_fdr.done"
  run:
    run_step(STEP_ID, output[0])
