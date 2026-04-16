configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_bigwig_chip"


rule all:
  input:
    "results/finish/make_bigwig_chip.done"


rule run_make_bigwig_chip:
  output:
    "results/finish/make_bigwig_chip.done"
  run:
    run_step(STEP_ID, output[0])
