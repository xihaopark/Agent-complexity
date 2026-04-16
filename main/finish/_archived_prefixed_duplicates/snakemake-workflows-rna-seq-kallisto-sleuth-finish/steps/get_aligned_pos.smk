configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_aligned_pos"


rule all:
  input:
    "results/finish/get_aligned_pos.done"


rule run_get_aligned_pos:
  output:
    "results/finish/get_aligned_pos.done"
  run:
    run_step(STEP_ID, output[0])
