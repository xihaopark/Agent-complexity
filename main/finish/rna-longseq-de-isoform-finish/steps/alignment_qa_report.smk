configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "alignment_qa_report"


rule all:
  input:
    "results/finish/alignment_qa_report.done"


rule run_alignment_qa_report:
  output:
    "results/finish/alignment_qa_report.done"
  run:
    run_step(STEP_ID, output[0])
