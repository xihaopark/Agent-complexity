configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prep_files_for_DEGs"


rule all:
  input:
    "results/finish/prep_files_for_DEGs.done"


rule run_prep_files_for_DEGs:
  output:
    "results/finish/prep_files_for_DEGs.done"
  run:
    run_step(STEP_ID, output[0])
