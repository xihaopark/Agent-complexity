configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "demultiplexing"


rule all:
  input:
    "results/finish/demultiplexing.done"


rule run_demultiplexing:
  output:
    "results/finish/demultiplexing.done"
  run:
    run_step(STEP_ID, output[0])
