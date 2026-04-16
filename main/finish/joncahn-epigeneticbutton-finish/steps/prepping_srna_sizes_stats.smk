configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prepping_srna_sizes_stats"


rule all:
  input:
    "results/finish/prepping_srna_sizes_stats.done"


rule run_prepping_srna_sizes_stats:
  output:
    "results/finish/prepping_srna_sizes_stats.done"
  run:
    run_step(STEP_ID, output[0])
