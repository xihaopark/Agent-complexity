configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3q_qualimapQC_dedup_STAR"


rule all:
  input:
    "results/finish/ilmn_3q_qualimapQC_dedup_STAR.done"


rule run_ilmn_3q_qualimapQC_dedup_STAR:
  output:
    "results/finish/ilmn_3q_qualimapQC_dedup_STAR.done"
  run:
    run_step(STEP_ID, output[0])
