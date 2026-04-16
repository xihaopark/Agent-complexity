configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "extract_reads_expression"


rule all:
  input:
    "results/finish/extract_reads_expression.done"


rule run_extract_reads_expression:
  output:
    "results/finish/extract_reads_expression.done"
  run:
    run_step(STEP_ID, output[0])
