configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calc_precision_recall"


rule all:
  input:
    "results/finish/calc_precision_recall.done"


rule run_calc_precision_recall:
  output:
    "results/finish/calc_precision_recall.done"
  run:
    run_step(STEP_ID, output[0])
