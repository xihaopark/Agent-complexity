configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_rna_se"


rule all:
  input:
    "results/finish/filter_rna_se.done"


rule run_filter_rna_se:
  output:
    "results/finish/filter_rna_se.done"
  run:
    run_step(STEP_ID, output[0])
