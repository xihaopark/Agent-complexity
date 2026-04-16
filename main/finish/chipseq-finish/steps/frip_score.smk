configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "frip_score"


rule all:
  input:
    "results/finish/frip_score.done"


rule run_frip_score:
  output:
    "results/finish/frip_score.done"
  run:
    run_step(STEP_ID, output[0])
