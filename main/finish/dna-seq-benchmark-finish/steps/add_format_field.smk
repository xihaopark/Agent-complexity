configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "add_format_field"


rule all:
  input:
    "results/finish/add_format_field.done"


rule run_add_format_field:
  output:
    "results/finish/add_format_field.done"
  run:
    run_step(STEP_ID, output[0])
