configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2b_txome_oarfish_quant"


rule all:
  input:
    "results/finish/ont_2b_txome_oarfish_quant.done"


rule run_ont_2b_txome_oarfish_quant:
  output:
    "results/finish/ont_2b_txome_oarfish_quant.done"
  run:
    run_step(STEP_ID, output[0])
