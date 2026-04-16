configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sm_rep_frip_score"


rule all:
  input:
    "results/finish/sm_rep_frip_score.done"


rule run_sm_rep_frip_score:
  output:
    "results/finish/sm_rep_frip_score.done"
  run:
    run_step(STEP_ID, output[0])
