configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_peak_stats"


rule all:
  input:
    "results/finish/make_peak_stats.done"


rule run_make_peak_stats:
  output:
    "results/finish/make_peak_stats.done"
  run:
    run_step(STEP_ID, output[0])
