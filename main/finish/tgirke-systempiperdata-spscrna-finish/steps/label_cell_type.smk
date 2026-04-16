configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "label_cell_type"


rule all:
  input:
    "results/finish/label_cell_type.done"


rule run_label_cell_type:
  output:
    "results/finish/label_cell_type.done"
  run:
    run_step(STEP_ID, output[0])
