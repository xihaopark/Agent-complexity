configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "symlink_stats"


rule all:
  input:
    "results/finish/symlink_stats.done"


rule run_symlink_stats:
  output:
    "results/finish/symlink_stats.done"
  run:
    run_step(STEP_ID, output[0])
