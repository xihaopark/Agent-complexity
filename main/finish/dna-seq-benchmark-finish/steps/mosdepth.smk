configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "mosdepth"


rule all:
  input:
    "results/finish/mosdepth.done"


rule run_mosdepth:
  output:
    "results/finish/mosdepth.done"
  run:
    run_step(STEP_ID, output[0])
