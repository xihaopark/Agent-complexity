configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "idr_analysis_replicates"


rule all:
  input:
    "results/finish/idr_analysis_replicates.done"


rule run_idr_analysis_replicates:
  output:
    "results/finish/idr_analysis_replicates.done"
  run:
    run_step(STEP_ID, output[0])
