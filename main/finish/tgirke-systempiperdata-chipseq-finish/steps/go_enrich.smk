configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "go_enrich"


rule all:
  input:
    "results/finish/go_enrich.done"


rule run_go_enrich:
  output:
    "results/finish/go_enrich.done"
  run:
    run_step(STEP_ID, output[0])
