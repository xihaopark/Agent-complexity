configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "patch_segmentation_proseg"


rule all:
  input:
    "results/finish/patch_segmentation_proseg.done"


rule run_patch_segmentation_proseg:
  output:
    "results/finish/patch_segmentation_proseg.done"
  run:
    run_step(STEP_ID, output[0])
