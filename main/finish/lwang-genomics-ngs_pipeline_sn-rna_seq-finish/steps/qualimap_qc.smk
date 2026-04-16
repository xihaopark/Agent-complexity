configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "qualimap_qc"


rule all:
  input:
    "results/finish/qualimap_qc.done"


rule run_qualimap_qc:
  output:
    "results/finish/qualimap_qc.done"
  run:
    run_step(STEP_ID, output[0])
