configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_bed"


rule all:
  input:
    "results/finish/make_bed.done"


rule run_make_bed:
  output:
    "results/finish/make_bed.done"
  run:
    run_step(STEP_ID, output[0])
