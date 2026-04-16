configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fetch_file"


rule all:
  input:
    "results/finish/fetch_file.done"


rule run_fetch_file:
  output:
    "results/finish/fetch_file.done"
  run:
    run_step(STEP_ID, output[0])
