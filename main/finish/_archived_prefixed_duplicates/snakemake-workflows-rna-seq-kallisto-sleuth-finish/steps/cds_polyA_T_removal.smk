configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cds_polyA_T_removal"


rule all:
  input:
    "results/finish/cds_polyA_T_removal.done"


rule run_cds_polyA_T_removal:
  output:
    "results/finish/cds_polyA_T_removal.done"
  run:
    run_step(STEP_ID, output[0])
