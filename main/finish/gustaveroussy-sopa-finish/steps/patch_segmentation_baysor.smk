configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "patch_segmentation_baysor"


rule all:
  input:
    "results/finish/patch_segmentation_baysor.done"


rule run_patch_segmentation_baysor:
  output:
    "results/finish/patch_segmentation_baysor.done"
  run:
    run_step(STEP_ID, output[0])
