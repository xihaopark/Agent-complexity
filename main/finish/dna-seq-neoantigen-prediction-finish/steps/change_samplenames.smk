configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "change_samplenames"


rule all:
  input:
    "results/finish/change_samplenames.done"


rule run_change_samplenames:
  output:
    "results/finish/change_samplenames.done"
  run:
    run_step(STEP_ID, output[0])
