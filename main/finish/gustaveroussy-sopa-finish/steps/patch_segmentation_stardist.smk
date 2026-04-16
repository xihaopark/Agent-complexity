configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "patch_segmentation_stardist"


rule all:
  input:
    "results/finish/patch_segmentation_stardist.done"


rule run_patch_segmentation_stardist:
  output:
    "results/finish/patch_segmentation_stardist.done"
  run:
    run_step(STEP_ID, output[0])
