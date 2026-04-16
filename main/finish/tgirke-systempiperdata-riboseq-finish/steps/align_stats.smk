configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "align_stats"


rule all:
  input:
    "results/finish/align_stats.done"


rule run_align_stats:
  output:
    "results/finish/align_stats.done"
  run:
    run_step(STEP_ID, output[0])
