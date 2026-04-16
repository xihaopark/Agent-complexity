configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "run_pipeline"


rule all:
  input:
    "results/finish/run_pipeline.done"


rule run_run_pipeline:
  output:
    "results/finish/run_pipeline.done"
  run:
    run_step(STEP_ID, output[0])
