configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "build_germline_proteome"


rule all:
  input:
    "results/finish/build_germline_proteome.done"


rule run_build_germline_proteome:
  output:
    "results/finish/build_germline_proteome.done"
  run:
    run_step(STEP_ID, output[0])
