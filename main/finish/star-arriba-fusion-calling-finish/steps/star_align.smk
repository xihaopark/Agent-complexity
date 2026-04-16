configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "star_align"


rule all:
  input:
    "results/finish/star_align.done"


rule run_star_align:
  output:
    "results/finish/star_align.done"
  run:
    run_step(STEP_ID, output[0])
