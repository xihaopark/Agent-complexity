configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "spoof_t2g"


rule all:
  input:
    "results/finish/spoof_t2g.done"


rule run_spoof_t2g:
  output:
    "results/finish/spoof_t2g.done"
  run:
    run_step(STEP_ID, output[0])
