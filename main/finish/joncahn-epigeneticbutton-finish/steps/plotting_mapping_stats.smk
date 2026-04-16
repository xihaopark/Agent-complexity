configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotting_mapping_stats"


rule all:
  input:
    "results/finish/plotting_mapping_stats.done"


rule run_plotting_mapping_stats:
  output:
    "results/finish/plotting_mapping_stats.done"
  run:
    run_step(STEP_ID, output[0])
