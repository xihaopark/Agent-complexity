configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "call_DMRs_pairwise"


rule all:
  input:
    "results/finish/call_DMRs_pairwise.done"


rule run_call_DMRs_pairwise:
  output:
    "results/finish/call_DMRs_pairwise.done"
  run:
    run_step(STEP_ID, output[0])
