configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "parse_regulatory_build"


rule all:
  input:
    "results/finish/parse_regulatory_build.done"


rule run_parse_regulatory_build:
  output:
    "results/finish/parse_regulatory_build.done"
  run:
    run_step(STEP_ID, output[0])
