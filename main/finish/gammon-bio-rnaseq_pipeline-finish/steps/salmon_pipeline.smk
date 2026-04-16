configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "salmon_pipeline"


rule all:
  input:
    "results/finish/salmon_pipeline.done"


rule run_salmon_pipeline:
  output:
    "results/finish/salmon_pipeline.done"
  run:
    run_step(STEP_ID, output[0])
