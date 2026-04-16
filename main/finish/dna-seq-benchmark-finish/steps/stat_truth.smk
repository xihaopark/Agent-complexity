configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "stat_truth"


rule all:
  input:
    "results/finish/stat_truth.done"


rule run_stat_truth:
  output:
    "results/finish/stat_truth.done"
  run:
    run_step(STEP_ID, output[0])
