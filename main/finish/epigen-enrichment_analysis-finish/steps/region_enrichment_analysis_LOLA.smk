configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "region_enrichment_analysis_LOLA"


rule all:
  input:
    "results/finish/region_enrichment_analysis_LOLA.done"


rule run_region_enrichment_analysis_LOLA:
  output:
    "results/finish/region_enrichment_analysis_LOLA.done"
  run:
    run_step(STEP_ID, output[0])
