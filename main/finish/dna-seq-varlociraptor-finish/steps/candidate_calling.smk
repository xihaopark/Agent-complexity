configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "candidate_calling"


rule all:
  input:
    "results/finish/candidate_calling.done"


rule run_candidate_calling:
  output:
    "results/finish/candidate_calling.done"
  run:
    run_step(STEP_ID, output[0])
