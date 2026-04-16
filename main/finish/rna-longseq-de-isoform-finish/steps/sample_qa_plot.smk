configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sample_qa_plot"


rule all:
  input:
    "results/finish/sample_qa_plot.done"


rule run_sample_qa_plot:
  output:
    "results/finish/sample_qa_plot.done"
  run:
    run_step(STEP_ID, output[0])
