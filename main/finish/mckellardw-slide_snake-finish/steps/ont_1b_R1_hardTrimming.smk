configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1b_R1_hardTrimming"


rule all:
  input:
    "results/finish/ont_1b_R1_hardTrimming.done"


rule run_ont_1b_R1_hardTrimming:
  output:
    "results/finish/ont_1b_R1_hardTrimming.done"
  run:
    run_step(STEP_ID, output[0])
