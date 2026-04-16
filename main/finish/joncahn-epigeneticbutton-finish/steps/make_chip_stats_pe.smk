configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_chip_stats_pe"


rule all:
  input:
    "results/finish/make_chip_stats_pe.done"


rule run_make_chip_stats_pe:
  output:
    "results/finish/make_chip_stats_pe.done"
  run:
    run_step(STEP_ID, output[0])
