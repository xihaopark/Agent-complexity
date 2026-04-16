configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "SingleCellRnaSeqMetricsCollector_species"


rule all:
  input:
    "results/finish/SingleCellRnaSeqMetricsCollector_species.done"


rule run_SingleCellRnaSeqMetricsCollector_species:
  output:
    "results/finish/SingleCellRnaSeqMetricsCollector_species.done"
  run:
    run_step(STEP_ID, output[0])
