configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_size_srna_sample"


rule all:
  input:
    "results/finish/filter_size_srna_sample.done"


rule run_filter_size_srna_sample:
  output:
    "results/finish/filter_size_srna_sample.done"
  run:
    run_step(STEP_ID, output[0])
