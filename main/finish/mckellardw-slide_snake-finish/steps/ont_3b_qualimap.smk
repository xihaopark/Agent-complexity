configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3b_qualimap"


rule all:
  input:
    "results/finish/ont_3b_qualimap.done"


rule run_ont_3b_qualimap:
  output:
    "results/finish/ont_3b_qualimap.done"
  run:
    run_step(STEP_ID, output[0])
