configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_fingerprint_plot"


rule all:
  input:
    "results/finish/make_fingerprint_plot.done"


rule run_make_fingerprint_plot:
  output:
    "results/finish/make_fingerprint_plot.done"
  run:
    run_step(STEP_ID, output[0])
