configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "wgbs_tools_pat_beta"


rule all:
  input:
    "results/finish/wgbs_tools_pat_beta.done"


rule run_wgbs_tools_pat_beta:
  output:
    "results/finish/wgbs_tools_pat_beta.done"
  run:
    run_step(STEP_ID, output[0])
