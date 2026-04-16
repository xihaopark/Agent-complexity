configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_protein_names"


rule all:
  input:
    "results/finish/get_protein_names.done"


rule run_get_protein_names:
  output:
    "results/finish/get_protein_names.done"
  run:
    run_step(STEP_ID, output[0])
