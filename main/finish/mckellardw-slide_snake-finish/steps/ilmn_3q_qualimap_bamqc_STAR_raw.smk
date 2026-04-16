configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3q_qualimap_bamqc_STAR_raw"


rule all:
  input:
    "results/finish/ilmn_3q_qualimap_bamqc_STAR_raw.done"


rule run_ilmn_3q_qualimap_bamqc_STAR_raw:
  output:
    "results/finish/ilmn_3q_qualimap_bamqc_STAR_raw.done"
  run:
    run_step(STEP_ID, output[0])
