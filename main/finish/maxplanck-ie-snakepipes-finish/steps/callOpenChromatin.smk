configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "callOpenChromatin"


rule all:
  input:
    "results/finish/callOpenChromatin.done"


rule run_callOpenChromatin:
  output:
    "results/finish/callOpenChromatin.done"
  run:
    run_step(STEP_ID, output[0])
