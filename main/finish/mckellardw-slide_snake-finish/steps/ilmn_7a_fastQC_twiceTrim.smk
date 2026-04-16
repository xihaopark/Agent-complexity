configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7a_fastQC_twiceTrim"


rule all:
  input:
    "results/finish/ilmn_7a_fastQC_twiceTrim.done"


rule run_ilmn_7a_fastQC_twiceTrim:
  output:
    "results/finish/ilmn_7a_fastQC_twiceTrim.done"
  run:
    run_step(STEP_ID, output[0])
