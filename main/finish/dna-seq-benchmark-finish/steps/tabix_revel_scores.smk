configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "tabix_revel_scores"


rule all:
  input:
    "results/finish/tabix_revel_scores.done"


rule run_tabix_revel_scores:
  output:
    "results/finish/tabix_revel_scores.done"
  run:
    run_step(STEP_ID, output[0])
