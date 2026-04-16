configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "tissue_segmentation"


rule all:
  input:
    "results/finish/tissue_segmentation.done"


rule run_tissue_segmentation:
  output:
    "results/finish/tissue_segmentation.done"
  run:
    run_step(STEP_ID, output[0])
