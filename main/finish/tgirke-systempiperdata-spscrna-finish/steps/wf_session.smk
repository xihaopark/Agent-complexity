configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "wf_session"


rule all:
  input:
    "results/finish/wf_session.done"


rule run_wf_session:
  output:
    "results/finish/wf_session.done"
  run:
    run_step(STEP_ID, output[0])
