configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "patch_segmentation_cellpose"


rule all:
  input:
    "results/finish/patch_segmentation_cellpose.done"


rule run_patch_segmentation_cellpose:
  output:
    "results/finish/patch_segmentation_cellpose.done"
  run:
    run_step(STEP_ID, output[0])
