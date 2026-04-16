configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_rna_stats_se"


rule all:
  input:
    "results/finish/make_rna_stats_se.done"


rule run_make_rna_stats_se:
  output:
    "results/finish/make_rna_stats_se.done"
  run:
    run_step(STEP_ID, output[0])
