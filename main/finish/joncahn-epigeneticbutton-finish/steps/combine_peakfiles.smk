configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "combine_peakfiles"


rule all:
  input:
    "results/finish/combine_peakfiles.done"


rule run_combine_peakfiles:
  output:
    "results/finish/combine_peakfiles.done"
  run:
    run_step(STEP_ID, output[0])
