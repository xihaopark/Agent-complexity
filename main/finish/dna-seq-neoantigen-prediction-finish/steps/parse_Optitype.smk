configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "parse_Optitype"


rule all:
  input:
    "results/finish/parse_Optitype.done"


rule run_parse_Optitype:
  output:
    "results/finish/parse_Optitype.done"
  run:
    run_step(STEP_ID, output[0])
