configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "parse_mhc_out"


rule all:
  input:
    "results/finish/parse_mhc_out.done"


rule run_parse_mhc_out:
  output:
    "results/finish/parse_mhc_out.done"
  run:
    run_step(STEP_ID, output[0])
