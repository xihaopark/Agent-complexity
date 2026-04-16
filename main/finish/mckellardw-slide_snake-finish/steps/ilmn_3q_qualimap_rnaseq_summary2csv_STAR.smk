configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3q_qualimap_rnaseq_summary2csv_STAR"


rule all:
  input:
    "results/finish/ilmn_3q_qualimap_rnaseq_summary2csv_STAR.done"


rule run_ilmn_3q_qualimap_rnaseq_summary2csv_STAR:
  output:
    "results/finish/ilmn_3q_qualimap_rnaseq_summary2csv_STAR.done"
  run:
    run_step(STEP_ID, output[0])
