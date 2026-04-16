configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "quantify_support_sample"


rule all:
  input:
    "results/finish/quantify_support_sample.done"


rule run_quantify_support_sample:
  output:
    "results/finish/quantify_support_sample.done"
  run:
    run_step(STEP_ID, output[0])
