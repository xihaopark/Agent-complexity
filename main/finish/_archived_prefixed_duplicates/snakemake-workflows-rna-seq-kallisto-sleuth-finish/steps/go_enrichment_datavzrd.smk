configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "go_enrichment_datavzrd"


rule all:
  input:
    "results/finish/go_enrichment_datavzrd.done"


rule run_go_enrichment_datavzrd:
  output:
    "results/finish/go_enrichment_datavzrd.done"
  run:
    run_step(STEP_ID, output[0])
