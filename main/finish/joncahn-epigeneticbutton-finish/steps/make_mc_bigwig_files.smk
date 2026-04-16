configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_mc_bigwig_files"


rule all:
  input:
    "results/finish/make_mc_bigwig_files.done"


rule run_make_mc_bigwig_files:
  output:
    "results/finish/make_mc_bigwig_files.done"
  run:
    run_step(STEP_ID, output[0])
