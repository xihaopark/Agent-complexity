configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_counts_long2mtx"


rule all:
  input:
    "results/finish/ilmn_3u_counts_long2mtx.done"


rule run_ilmn_3u_counts_long2mtx:
  output:
    "results/finish/ilmn_3u_counts_long2mtx.done"
  run:
    run_step(STEP_ID, output[0])
