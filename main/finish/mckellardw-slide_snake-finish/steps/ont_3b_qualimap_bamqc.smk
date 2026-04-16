configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3b_qualimap_bamqc"


rule all:
  input:
    "results/finish/ont_3b_qualimap_bamqc.done"


rule run_ont_3b_qualimap_bamqc:
  output:
    "results/finish/ont_3b_qualimap_bamqc.done"
  run:
    run_step(STEP_ID, output[0])
