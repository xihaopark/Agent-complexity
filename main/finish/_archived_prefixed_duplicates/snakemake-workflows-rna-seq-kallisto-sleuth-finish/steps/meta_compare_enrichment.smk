configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "meta_compare_enrichment"


rule all:
  input:
    "results/finish/meta_compare_enrichment.done"


rule run_meta_compare_enrichment:
  output:
    "results/finish/meta_compare_enrichment.done"
  run:
    run_step(STEP_ID, output[0])
