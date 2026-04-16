configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "summarize_pipeline"


rule all:
  input:
    "results/finish/summarize_pipeline.done"


rule run_summarize_pipeline:
  output:
    "results/finish/summarize_pipeline.done"
  run:
    run_step(STEP_ID, output[0])
