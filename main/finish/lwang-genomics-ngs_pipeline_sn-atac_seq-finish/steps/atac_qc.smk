configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "atac_qc"


rule all:
  input:
    "results/finish/atac_qc.done"


rule run_atac_qc:
  output:
    "results/finish/atac_qc.done"
  run:
    run_step(STEP_ID, output[0])
