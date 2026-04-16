configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_unmapped_primers"


rule all:
  input:
    "results/finish/filter_unmapped_primers.done"


rule run_filter_unmapped_primers:
  output:
    "results/finish/filter_unmapped_primers.done"
  run:
    run_step(STEP_ID, output[0])
