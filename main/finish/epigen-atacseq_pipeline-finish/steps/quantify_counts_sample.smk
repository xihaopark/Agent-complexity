configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "quantify_counts_sample"


rule all:
  input:
    "results/finish/quantify_counts_sample.done"


rule run_quantify_counts_sample:
  output:
    "results/finish/quantify_counts_sample.done"
  run:
    run_step(STEP_ID, output[0])
