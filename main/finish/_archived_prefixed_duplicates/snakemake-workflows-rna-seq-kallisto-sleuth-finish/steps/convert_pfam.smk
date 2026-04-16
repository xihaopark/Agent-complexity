configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "convert_pfam"


rule all:
  input:
    "results/finish/convert_pfam.done"


rule run_convert_pfam:
  output:
    "results/finish/convert_pfam.done"
  run:
    run_step(STEP_ID, output[0])
