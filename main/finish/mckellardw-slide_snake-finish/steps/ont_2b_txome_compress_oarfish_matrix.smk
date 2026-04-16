configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2b_txome_compress_oarfish_matrix"


rule all:
  input:
    "results/finish/ont_2b_txome_compress_oarfish_matrix.done"


rule run_ont_2b_txome_compress_oarfish_matrix:
  output:
    "results/finish/ont_2b_txome_compress_oarfish_matrix.done"
  run:
    run_step(STEP_ID, output[0])
