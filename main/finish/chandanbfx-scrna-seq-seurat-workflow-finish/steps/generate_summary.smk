configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "generate_summary"


rule all:
  input:
    "results/finish/generate_summary.done"


rule run_generate_summary:
  output:
    "results/finish/generate_summary.done"
  run:
    run_step(STEP_ID, output[0])
