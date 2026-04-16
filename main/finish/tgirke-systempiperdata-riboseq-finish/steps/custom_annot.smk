configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "custom_annot"


rule all:
  input:
    "results/finish/custom_annot.done"


rule run_custom_annot:
  output:
    "results/finish/custom_annot.done"
  run:
    run_step(STEP_ID, output[0])
