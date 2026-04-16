configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "reheader_filtered_bcf"


rule all:
  input:
    "results/finish/reheader_filtered_bcf.done"


rule run_reheader_filtered_bcf:
  output:
    "results/finish/reheader_filtered_bcf.done"
  run:
    run_step(STEP_ID, output[0])
