configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3u_tagReads"


rule all:
  input:
    "results/finish/ilmn_3u_tagReads.done"


rule run_ilmn_3u_tagReads:
  output:
    "results/finish/ilmn_3u_tagReads.done"
  run:
    run_step(STEP_ID, output[0])
