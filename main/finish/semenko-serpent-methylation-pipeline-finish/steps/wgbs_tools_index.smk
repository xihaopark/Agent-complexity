configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "wgbs_tools_index"


rule all:
  input:
    "results/finish/wgbs_tools_index.done"


rule run_wgbs_tools_index:
  output:
    "results/finish/wgbs_tools_index.done"
  run:
    run_step(STEP_ID, output[0])
