configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "total_sample_qa_plot"


rule all:
  input:
    "results/finish/total_sample_qa_plot.done"


rule run_total_sample_qa_plot:
  output:
    "results/finish/total_sample_qa_plot.done"
  run:
    run_step(STEP_ID, output[0])
