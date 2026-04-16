configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_filter_noGN"


rule all:
  input:
    "results/finish/ilmn_3u_filter_noGN.done"


rule run_ilmn_3u_filter_noGN:
  output:
    "results/finish/ilmn_3u_filter_noGN.done"
  run:
    run_step(STEP_ID, output[0])
