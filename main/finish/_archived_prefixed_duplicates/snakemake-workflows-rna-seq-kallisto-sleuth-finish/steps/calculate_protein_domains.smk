configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "calculate_protein_domains"


rule all:
  input:
    "results/finish/calculate_protein_domains.done"


rule run_calculate_protein_domains:
  output:
    "results/finish/calculate_protein_domains.done"
  run:
    run_step(STEP_ID, output[0])
