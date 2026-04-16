configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_extract_HMM_expression"


rule all:
  input:
    "results/finish/ilmn_3u_extract_HMM_expression.done"


rule run_ilmn_3u_extract_HMM_expression:
  output:
    "results/finish/ilmn_3u_extract_HMM_expression.done"
  run:
    run_step(STEP_ID, output[0])
