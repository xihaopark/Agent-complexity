configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "collect_precision_recall"


rule all:
  input:
    "results/finish/collect_precision_recall.done"


rule run_collect_precision_recall:
  output:
    "results/finish/collect_precision_recall.done"
  run:
    run_step(STEP_ID, output[0])
