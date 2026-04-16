configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3b_qualimap_bamqc_summary2csv"


rule all:
  input:
    "results/finish/ont_3b_qualimap_bamqc_summary2csv.done"


rule run_ont_3b_qualimap_bamqc_summary2csv:
  output:
    "results/finish/ont_3b_qualimap_bamqc_summary2csv.done"
  run:
    run_step(STEP_ID, output[0])
