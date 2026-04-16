configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ilmn_7b_readQC_downsample"


rule all:
  input:
    "results/finish/ilmn_7b_readQC_downsample.done"


rule run_ilmn_7b_readQC_downsample:
  output:
    "results/finish/ilmn_7b_readQC_downsample.done"
  run:
    run_step(STEP_ID, output[0])
