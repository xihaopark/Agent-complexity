configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "phantompeakqualtools"


rule all:
  input:
    "results/finish/phantompeakqualtools.done"


rule run_phantompeakqualtools:
  output:
    "results/finish/phantompeakqualtools.done"
  run:
    run_step(STEP_ID, output[0])
