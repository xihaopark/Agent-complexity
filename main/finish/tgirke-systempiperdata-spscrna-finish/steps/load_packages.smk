configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "load_packages"


rule all:
  input:
    "results/finish/load_packages.done"


rule run_load_packages:
  output:
    "results/finish/load_packages.done"
  run:
    run_step(STEP_ID, output[0])
