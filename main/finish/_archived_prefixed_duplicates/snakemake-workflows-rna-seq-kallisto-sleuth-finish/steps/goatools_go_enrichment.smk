configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "goatools_go_enrichment"


rule all:
  input:
    "results/finish/goatools_go_enrichment.done"


rule run_goatools_go_enrichment:
  output:
    "results/finish/goatools_go_enrichment.done"
  run:
    run_step(STEP_ID, output[0])
