configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "region_motif_enrichment_analysis_pycisTarget"


rule all:
  input:
    "results/finish/region_motif_enrichment_analysis_pycisTarget.done"


rule run_region_motif_enrichment_analysis_pycisTarget:
  output:
    "results/finish/region_motif_enrichment_analysis_pycisTarget.done"
  run:
    run_step(STEP_ID, output[0])
