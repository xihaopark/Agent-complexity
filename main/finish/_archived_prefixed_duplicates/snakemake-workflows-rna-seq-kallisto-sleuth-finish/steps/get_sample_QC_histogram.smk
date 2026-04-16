configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_sample_QC_histogram"


rule all:
  input:
    "results/finish/get_sample_QC_histogram.done"


rule run_get_sample_QC_histogram:
  output:
    "results/finish/get_sample_QC_histogram.done"
  run:
    run_step(STEP_ID, output[0])
