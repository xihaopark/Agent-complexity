configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "patch_segmentation_comseg"


rule all:
  input:
    "results/finish/patch_segmentation_comseg.done"


rule run_patch_segmentation_comseg:
  output:
    "results/finish/patch_segmentation_comseg.done"
  run:
    run_step(STEP_ID, output[0])
