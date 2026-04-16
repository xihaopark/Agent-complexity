configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "postprocess_target_bed"


rule all:
  input:
    "results/finish/postprocess_target_bed.done"


rule run_postprocess_target_bed:
  output:
    "results/finish/postprocess_target_bed.done"
  run:
    run_step(STEP_ID, output[0])
