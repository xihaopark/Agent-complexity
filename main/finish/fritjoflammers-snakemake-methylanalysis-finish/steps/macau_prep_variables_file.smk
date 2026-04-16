configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "macau_prep_variables_file"


rule all:
  input:
    "results/finish/macau_prep_variables_file.done"


rule run_macau_prep_variables_file:
  output:
    "results/finish/macau_prep_variables_file.done"
  run:
    run_step(STEP_ID, output[0])
