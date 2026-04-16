configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "parse_HLA_LA"


rule all:
  input:
    "results/finish/parse_HLA_LA.done"


rule run_parse_HLA_LA:
  output:
    "results/finish/parse_HLA_LA.done"
  run:
    run_step(STEP_ID, output[0])
