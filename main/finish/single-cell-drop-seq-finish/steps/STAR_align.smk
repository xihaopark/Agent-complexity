configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "STAR_align"


rule all:
  input:
    "results/finish/STAR_align.done"


rule run_STAR_align:
  output:
    "results/finish/STAR_align.done"
  run:
    run_step(STEP_ID, output[0])
