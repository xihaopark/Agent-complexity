configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2a_umitools_count"


rule all:
  input:
    "results/finish/ont_2a_umitools_count.done"


rule run_ont_2a_umitools_count:
  output:
    "results/finish/ont_2a_umitools_count.done"
  run:
    run_step(STEP_ID, output[0])
