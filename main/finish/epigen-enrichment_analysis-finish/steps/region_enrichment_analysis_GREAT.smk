configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "region_enrichment_analysis_GREAT"


rule all:
  input:
    "results/finish/region_enrichment_analysis_GREAT.done"


rule run_region_enrichment_analysis_GREAT:
  output:
    "results/finish/region_enrichment_analysis_GREAT.done"
  run:
    run_step(STEP_ID, output[0])
