configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2b_txome_sort_by_xb"


rule all:
  input:
    "results/finish/ont_2b_txome_sort_by_xb.done"


rule run_ont_2b_txome_sort_by_xb:
  output:
    "results/finish/ont_2b_txome_sort_by_xb.done"
  run:
    run_step(STEP_ID, output[0])
