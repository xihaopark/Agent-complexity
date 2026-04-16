configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "SingleCellRnaSeqMetricsCollector"


rule all:
  input:
    "results/finish/SingleCellRnaSeqMetricsCollector.done"


rule run_SingleCellRnaSeqMetricsCollector:
  output:
    "results/finish/SingleCellRnaSeqMetricsCollector.done"
  run:
    run_step(STEP_ID, output[0])
