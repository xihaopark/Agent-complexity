configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "download_regulatory_annotation"


rule all:
  input:
    "results/finish/download_regulatory_annotation.done"


rule run_download_regulatory_annotation:
  output:
    "results/finish/download_regulatory_annotation.done"
  run:
    run_step(STEP_ID, output[0])
