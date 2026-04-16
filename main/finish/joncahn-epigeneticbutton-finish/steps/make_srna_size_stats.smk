configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_srna_size_stats"


rule all:
  input:
    "results/finish/make_srna_size_stats.done"


rule run_make_srna_size_stats:
  output:
    "results/finish/make_srna_size_stats.done"
  run:
    run_step(STEP_ID, output[0])
