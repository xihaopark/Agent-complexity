configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "combined_analysis"


rule all:
  input:
    "results/finish/combined_analysis.done"


rule run_combined_analysis:
  output:
    "results/finish/combined_analysis.done"
  run:
    run_step(STEP_ID, output[0])
