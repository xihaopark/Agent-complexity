configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "install_homer"


rule all:
  input:
    "results/finish/install_homer.done"


rule run_install_homer:
  output:
    "results/finish/install_homer.done"
  run:
    run_step(STEP_ID, output[0])
