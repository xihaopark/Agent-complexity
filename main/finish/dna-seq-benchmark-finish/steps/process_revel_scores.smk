configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "process_revel_scores"


rule all:
  input:
    "results/finish/process_revel_scores.done"


rule run_process_revel_scores:
  output:
    "results/finish/process_revel_scores.done"
  run:
    run_step(STEP_ID, output[0])
