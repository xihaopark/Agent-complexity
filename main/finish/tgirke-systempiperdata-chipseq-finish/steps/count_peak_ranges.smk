configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "count_peak_ranges"


rule all:
  input:
    "results/finish/count_peak_ranges.done"


rule run_count_peak_ranges:
  output:
    "results/finish/count_peak_ranges.done"
  run:
    run_step(STEP_ID, output[0])
