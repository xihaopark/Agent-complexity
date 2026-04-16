configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "compose_sample_sheet"


rule all:
  input:
    "results/finish/compose_sample_sheet.done"


rule run_compose_sample_sheet:
  output:
    "results/finish/compose_sample_sheet.done"
  run:
    run_step(STEP_ID, output[0])
