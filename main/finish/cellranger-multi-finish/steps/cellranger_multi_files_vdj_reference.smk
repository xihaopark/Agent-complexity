configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cellranger_multi_files_vdj_reference"


rule all:
  input:
    "results/finish/cellranger_multi_files_vdj_reference.done"


rule run_cellranger_multi_files_vdj_reference:
  output:
    "results/finish/cellranger_multi_files_vdj_reference.done"
  run:
    run_step(STEP_ID, output[0])
