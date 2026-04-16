configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "collect_multiple_metrics"


rule all:
  input:
    "results/finish/collect_multiple_metrics.done"


rule run_collect_multiple_metrics:
  output:
    "results/finish/collect_multiple_metrics.done"
  run:
    run_step(STEP_ID, output[0])
