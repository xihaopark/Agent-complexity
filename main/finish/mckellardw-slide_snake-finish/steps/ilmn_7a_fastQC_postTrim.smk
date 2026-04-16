configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7a_fastQC_postTrim"


rule all:
  input:
    "results/finish/ilmn_7a_fastQC_postTrim.done"


rule run_ilmn_7a_fastQC_postTrim:
  output:
    "results/finish/ilmn_7a_fastQC_postTrim.done"
  run:
    run_step(STEP_ID, output[0])
