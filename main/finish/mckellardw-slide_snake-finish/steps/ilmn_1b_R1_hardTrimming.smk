configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_1b_R1_hardTrimming"


rule all:
  input:
    "results/finish/ilmn_1b_R1_hardTrimming.done"


rule run_ilmn_1b_R1_hardTrimming:
  output:
    "results/finish/ilmn_1b_R1_hardTrimming.done"
  run:
    run_step(STEP_ID, output[0])
