configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_rna_pe"


rule all:
  input:
    "results/finish/filter_rna_pe.done"


rule run_filter_rna_pe:
  output:
    "results/finish/filter_rna_pe.done"
  run:
    run_step(STEP_ID, output[0])
