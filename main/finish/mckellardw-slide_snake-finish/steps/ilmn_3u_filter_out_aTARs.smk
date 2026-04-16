configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_filter_out_aTARs"


rule all:
  input:
    "results/finish/ilmn_3u_filter_out_aTARs.done"


rule run_ilmn_3u_filter_out_aTARs:
  output:
    "results/finish/ilmn_3u_filter_out_aTARs.done"
  run:
    run_step(STEP_ID, output[0])
