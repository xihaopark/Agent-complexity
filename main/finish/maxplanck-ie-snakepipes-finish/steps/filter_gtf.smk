configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_gtf"


rule all:
  input:
    "results/finish/filter_gtf.done"


rule run_filter_gtf:
  output:
    "results/finish/filter_gtf.done"
  run:
    run_step(STEP_ID, output[0])
