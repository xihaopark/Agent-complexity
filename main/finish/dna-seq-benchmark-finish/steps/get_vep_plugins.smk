configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_vep_plugins"


rule all:
  input:
    "results/finish/get_vep_plugins.done"


rule run_get_vep_plugins:
  output:
    "results/finish/get_vep_plugins.done"
  run:
    run_step(STEP_ID, output[0])
