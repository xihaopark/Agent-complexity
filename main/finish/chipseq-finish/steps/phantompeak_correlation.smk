configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "phantompeak_correlation"


rule all:
  input:
    "results/finish/phantompeak_correlation.done"


rule run_phantompeak_correlation:
  output:
    "results/finish/phantompeak_correlation.done"
  run:
    run_step(STEP_ID, output[0])
