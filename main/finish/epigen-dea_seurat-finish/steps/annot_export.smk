configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annot_export"


rule all:
  input:
    "results/finish/annot_export.done"


rule run_annot_export:
  output:
    "results/finish/annot_export.done"
  run:
    run_step(STEP_ID, output[0])
