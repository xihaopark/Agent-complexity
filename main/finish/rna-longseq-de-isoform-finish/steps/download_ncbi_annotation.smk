configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "download_ncbi_annotation"


rule all:
  input:
    "results/finish/download_ncbi_annotation.done"


rule run_download_ncbi_annotation:
  output:
    "results/finish/download_ncbi_annotation.done"
  run:
    run_step(STEP_ID, output[0])
