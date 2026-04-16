configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7a_fastQC_preTrim"


rule all:
  input:
    "results/finish/ilmn_7a_fastQC_preTrim.done"


rule run_ilmn_7a_fastQC_preTrim:
  output:
    "results/finish/ilmn_7a_fastQC_preTrim.done"
  run:
    run_step(STEP_ID, output[0])
