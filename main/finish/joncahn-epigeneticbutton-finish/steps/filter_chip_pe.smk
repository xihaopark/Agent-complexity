configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_chip_pe"


rule all:
  input:
    "results/finish/filter_chip_pe.done"


rule run_filter_chip_pe:
  output:
    "results/finish/filter_chip_pe.done"
  run:
    run_step(STEP_ID, output[0])
