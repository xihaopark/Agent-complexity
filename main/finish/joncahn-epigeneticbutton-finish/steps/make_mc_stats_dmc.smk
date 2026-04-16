configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_mc_stats_dmc"


rule all:
  input:
    "results/finish/make_mc_stats_dmc.done"


rule run_make_mc_stats_dmc:
  output:
    "results/finish/make_mc_stats_dmc.done"
  run:
    run_step(STEP_ID, output[0])
