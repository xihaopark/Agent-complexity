configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "notebook_data_structure"


rule all:
  input:
    "results/finish/notebook_data_structure.done"


rule run_notebook_data_structure:
  output:
    "results/finish/notebook_data_structure.done"
  run:
    run_step(STEP_ID, output[0])
