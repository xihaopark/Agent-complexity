configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bcrank_enrich"


rule all:
  input:
    "results/finish/bcrank_enrich.done"


rule run_bcrank_enrich:
  output:
    "results/finish/bcrank_enrich.done"
  run:
    run_step(STEP_ID, output[0])
