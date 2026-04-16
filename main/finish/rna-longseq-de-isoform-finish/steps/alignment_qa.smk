configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "alignment_qa"


rule all:
  input:
    "results/finish/alignment_qa.done"


rule run_alignment_qa:
  output:
    "results/finish/alignment_qa.done"
  run:
    run_step(STEP_ID, output[0])
