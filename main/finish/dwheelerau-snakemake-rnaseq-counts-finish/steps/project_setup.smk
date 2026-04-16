configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "project_setup"


rule all:
  input:
    "results/finish/project_setup.done"


rule run_project_setup:
  output:
    "results/finish/project_setup.done"
  run:
    run_step(STEP_ID, output[0])
