configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "alignment_qc"


rule all:
  input:
    "results/finish/alignment_qc.done"


rule run_alignment_qc:
  output:
    "results/finish/alignment_qc.done"
  run:
    run_step(STEP_ID, output[0])
