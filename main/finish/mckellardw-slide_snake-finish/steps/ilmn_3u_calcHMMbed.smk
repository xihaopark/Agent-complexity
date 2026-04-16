configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_calcHMMbed"


rule all:
  input:
    "results/finish/ilmn_3u_calcHMMbed.done"


rule run_ilmn_3u_calcHMMbed:
  output:
    "results/finish/ilmn_3u_calcHMMbed.done"
  run:
    run_step(STEP_ID, output[0])
