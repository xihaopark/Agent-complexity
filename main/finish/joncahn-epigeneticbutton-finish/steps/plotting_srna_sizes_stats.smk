configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotting_srna_sizes_stats"


rule all:
  input:
    "results/finish/plotting_srna_sizes_stats.done"


rule run_plotting_srna_sizes_stats:
  output:
    "results/finish/plotting_srna_sizes_stats.done"
  run:
    run_step(STEP_ID, output[0])
