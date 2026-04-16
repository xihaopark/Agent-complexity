configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "check_gff"


rule all:
  input:
    "results/finish/check_gff.done"


rule run_check_gff:
  output:
    "results/finish/check_gff.done"
  run:
    run_step(STEP_ID, output[0])
