configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "summary_stats"


rule all:
  input:
    "results/finish/summary_stats.done"


rule run_summary_stats:
  output:
    "results/finish/summary_stats.done"
  run:
    run_step(STEP_ID, output[0])
