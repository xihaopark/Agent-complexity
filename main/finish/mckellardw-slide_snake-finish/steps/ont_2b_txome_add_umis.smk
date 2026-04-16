configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2b_txome_add_umis"


rule all:
  input:
    "results/finish/ont_2b_txome_add_umis.done"


rule run_ont_2b_txome_add_umis:
  output:
    "results/finish/ont_2b_txome_add_umis.done"
  run:
    run_step(STEP_ID, output[0])
