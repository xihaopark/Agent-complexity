configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_3a_compress_STAR_outs"


rule all:
  input:
    "results/finish/ilmn_3a_compress_STAR_outs.done"


rule run_ilmn_3a_compress_STAR_outs:
  output:
    "results/finish/ilmn_3a_compress_STAR_outs.done"
  run:
    run_step(STEP_ID, output[0])
