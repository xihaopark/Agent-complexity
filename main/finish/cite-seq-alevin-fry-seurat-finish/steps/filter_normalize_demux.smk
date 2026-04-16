configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filter_normalize_demux"


rule all:
  input:
    "results/finish/filter_normalize_demux.done"


rule run_filter_normalize_demux:
  output:
    "results/finish/filter_normalize_demux.done"
  run:
    run_step(STEP_ID, output[0])
