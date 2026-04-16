configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "patchify_image"


rule all:
  input:
    "results/finish/patchify_image.done"


rule run_patchify_image:
  output:
    "results/finish/patchify_image.done"
  run:
    run_step(STEP_ID, output[0])
