configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "standardize_gff"


rule all:
  input:
    "results/finish/standardize_gff.done"


rule run_standardize_gff:
  output:
    "results/finish/standardize_gff.done"
  run:
    run_step(STEP_ID, output[0])
