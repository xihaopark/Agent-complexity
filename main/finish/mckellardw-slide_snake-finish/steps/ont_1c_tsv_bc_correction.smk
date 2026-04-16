configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_1c_tsv_bc_correction"


rule all:
  input:
    "results/finish/ont_1c_tsv_bc_correction.done"


rule run_ont_1c_tsv_bc_correction:
  output:
    "results/finish/ont_1c_tsv_bc_correction.done"
  run:
    run_step(STEP_ID, output[0])
