configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "postprocess_go_enrichment"


rule all:
  input:
    "results/finish/postprocess_go_enrichment.done"


rule run_postprocess_go_enrichment:
  output:
    "results/finish/postprocess_go_enrichment.done"
  run:
    run_step(STEP_ID, output[0])
