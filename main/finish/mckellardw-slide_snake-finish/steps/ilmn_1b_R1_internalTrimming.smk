configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_1b_R1_internalTrimming"


rule all:
  input:
    "results/finish/ilmn_1b_R1_internalTrimming.done"


rule run_ilmn_1b_R1_internalTrimming:
  output:
    "results/finish/ilmn_1b_R1_internalTrimming.done"
  run:
    run_step(STEP_ID, output[0])
